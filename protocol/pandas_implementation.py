"""
Implementation of the dataframe exchange protocol.

Public API
----------

from_dataframe : construct a pandas.DataFrame from an input data frame which
                 implements the exchange protocol

Notes
-----

- Interpreting a raw pointer (as in ``Buffer.ptr``) is annoying and unsafe to
  do in pure Python. It's more general but definitely less friendly than having
  ``to_arrow`` and ``to_numpy`` methods. So for the buffers which lack
  ``__dlpack__`` (e.g., because the column dtype isn't supported by DLPack),
  this is worth looking at again.

"""

import enum
import collections
import ctypes
from typing import Any, Optional, Tuple, Dict, Iterable, Sequence

import pandas as pd
import numpy as np
import pandas._testing as tm
import pytest


# A typing protocol could be added later to let Mypy validate code using
# `from_dataframe` better.
DataFrameObject = Any
ColumnObject = Any


def from_dataframe(df : DataFrameObject) -> pd.DataFrame:
    """
    Construct a pandas DataFrame from ``df`` if it supports ``__dataframe__``
    """
    # NOTE: commented out for roundtrip testing
    # if isinstance(df, pd.DataFrame):
    #     return df

    if not hasattr(df, '__dataframe__'):
        raise ValueError("`df` does not support __dataframe__")

    return _from_dataframe(df.__dataframe__())


def _from_dataframe(df : DataFrameObject) -> pd.DataFrame:
    """
    Note: not all cases are handled yet, only ones that can be implemented with
    only Pandas. Later, we need to implement/test support for categoricals,
    bit/byte masks, chunk handling, etc.
    """
    # Check number of chunks, if there's more than one we need to iterate
    if df.num_chunks() > 1:
        raise NotImplementedError

    # We need a dict of columns here, with each column being a numpy array (at
    # least for now, deal with non-numpy dtypes later).
    columns = dict()
    for name in df.column_names():
        columns[name] = convert_column_to_ndarray(df.get_column_by_name(name))

    return pd.DataFrame(columns)


class _DtypeKind(enum.IntEnum):
    INT = 0
    UINT = 1
    FLOAT = 2
    BOOL = 20
    STRING = 21   # UTF-8
    DATETIME = 22
    CATEGORICAL = 23


def convert_column_to_ndarray(col : ColumnObject) -> np.ndarray:
    """
    """
    if col.offset != 0:
        raise NotImplementedError("column.offset > 0 not handled yet")

    if col.describe_null[0] not in (0, 1):
        raise NotImplementedError("Null values represented as masks or "
                                  "sentinel values not handled yet")

    # Handle the dtype
    _dtype = col.dtype
    kind = _dtype[0]
    bitwidth = _dtype[1]
    _k = _DtypeKind
    if _dtype[0] not in (_k.INT, _k.UINT, _k.FLOAT, _k.BOOL):
        raise RuntimeError("Not a boolean, integer or floating-point dtype")

    _ints = {8: np.int8, 16: np.int16, 32: np.int32, 64: np.int64}
    _uints = {8: np.uint8, 16: np.uint16, 32: np.uint32, 64: np.uint64}
    _floats = {32: np.float32, 64: np.float64}
    _np_dtypes = {0: _ints, 1: _uints, 2: _floats, 20: {8: bool}}
    column_dtype = _np_dtypes[kind][bitwidth]

    # No DLPack yet, so need to construct a new ndarray from the data pointer
    # and size in the buffer plus the dtype on the column
    _buffer = col.get_data_buffer()
    ctypes_type = np.ctypeslib.as_ctypes_type(column_dtype)
    data_pointer = ctypes.cast(_buffer.ptr, ctypes.POINTER(ctypes_type))

    # NOTE: `x` does not own its memory, so the caller of this function must
    #       either make a copy or hold on to a reference of the column or
    #       buffer! (not done yet, this is pretty awful ...)
    x = np.ctypeslib.as_array(data_pointer,
                              shape=(_buffer.bufsize // (bitwidth//8),))

    return x


def __dataframe__(cls, nan_as_null : bool = False) -> dict:
    """
    The public method to attach to pd.DataFrame

    We'll attach it via monkeypatching here for demo purposes. If Pandas adopt
    the protocol, this will be a regular method on pandas.DataFrame.

    ``nan_as_null`` is a keyword intended for the consumer to tell the
    producer to overwrite null values in the data with ``NaN`` (or ``NaT``).
    This currently has no effect; once support for nullable extension
    dtypes is added, this value should be propagated to columns.
    """
    return _PandasDataFrame(cls, nan_as_null=nan_as_null)


# Monkeypatch the Pandas DataFrame class to support the interchange protocol
pd.DataFrame.__dataframe__ = __dataframe__


# Implementation of interchange protocol
# --------------------------------------

class _PandasBuffer:
    """
    Data in the buffer is guaranteed to be contiguous in memory.
    """

    def __init__(self, x : np.ndarray) -> None:
        """
        Handle only regular columns (= numpy arrays) for now.
        """
        if not x.strides == (x.dtype.itemsize,):
            # Array is not contiguous - this is possible to get in Pandas,
            # there was some discussion on whether to support it. Som extra
            # complexity for libraries that don't support it (e.g. Arrow),
            # but would help with numpy-based libraries like Pandas.
            raise RuntimeError("Design needs fixing - non-contiguous buffer")

        # Store the numpy array in which the data resides as a private
        # attribute, so we can use it to retrieve the public attributes
        self._x = x

    @property
    def bufsize(self) -> int:
        """
        Buffer size in bytes
        """
        return self._x.size * self._x.dtype.itemsize

    @property
    def ptr(self) -> int:
        """
        Pointer to start of the buffer as an integer
        """
        return self._x.__array_interface__['data'][0]

    def __dlpack__(self):
        """
        DLPack not implemented in NumPy yet, so leave it out here
        """
        raise NotImplementedError("__dlpack__")

    def __dlpack_device__(self) -> Tuple[enum.IntEnum, int]:
        """
        Device type and device ID for where the data in the buffer resides.
        """
        class Device(enum.IntEnum):
            CPU = 1

        return (Device.CPU, None)


class _PandasColumn:
    """
    A column object, with only the methods and properties required by the
    interchange protocol defined.

    A column can contain one or more chunks. Each chunk can contain either one
    or two buffers - one data buffer and (depending on null representation) it
    may have a mask buffer.

    Note: this Column object can only be produced by ``__dataframe__``, so
          doesn't need its own version or ``__column__`` protocol.

    """

    def __init__(self, column : pd.Series) -> None:
        """
        Note: doesn't deal with extension arrays yet, just assume a regular
        Series/ndarray for now.
        """
        if not isinstance(column, pd.Series):
            raise NotImplementedError("Columns of type {} not handled "
                                      "yet".format(type(column)))

        # Store the column as a private attribute
        self._col = column

    @property
    def size(self) -> int:
        """
        Size of the column, in elements.
        """
        return self._col.size

    @property
    def offset(self) -> int:
        """
        Offset of first element. Always zero.
        """
        return 0

    @property
    def dtype(self) -> Tuple[enum.IntEnum, int, str, str]:
        """
        Dtype description as a tuple ``(kind, bit-width, format string, endianness)``

        Kind :

            - INT = 0
            - UINT = 1
            - FLOAT = 2
            - BOOL = 20
            - STRING = 21   # UTF-8
            - DATETIME = 22
            - CATEGORICAL = 23

        Bit-width : the number of bits as an integer
        Format string : data type description format string in Apache Arrow C
                        Data Interface format.
        Endianness : current only native endianness (``=``) is supported

        Notes:

            - Kind specifiers are aligned with DLPack where possible (hence the
              jump to 20, leave enough room for future extension)
            - Masks must be specified as boolean with either bit width 1 (for bit
              masks) or 8 (for byte masks).
            - Dtype width in bits was preferred over bytes
            - Endianness isn't too useful, but included now in case in the future
              we need to support non-native endianness
            - Went with Apache Arrow format strings over NumPy format strings
              because they're more complete from a dataframe perspective
            - Format strings are mostly useful for datetime specification, and
              for categoricals.
            - For categoricals, the format string describes the type of the
              categorical in the data buffer. In case of a separate encoding of
              the categorical (e.g. an integer to string mapping), this can
              be derived from ``self.describe_categorical``.
            - Data types not included: complex, Arrow-style null, binary, decimal,
              and nested (list, struct, map, union) dtypes.
        """
        dtype = self._col.dtype
        # Note: 'c' (complex) not handled yet (not in array spec v1).
        #       'b', 'B' (bytes), 'S', 'a', (old-style string) 'V' (void) not handled
        #       datetime and timedelta both map to datetime (is timedelta handled?)
        _k = _DtypeKind
        _np_kinds = {'i': _k.INT, 'u': _k.UINT, 'f': _k.FLOAT, 'b': _k.BOOL,
                     'U': _k.STRING,
                     'M': _k.DATETIME, 'm': _k.DATETIME}
        kind = _np_kinds.get(dtype.kind, None)
        if kind is None:
            # Not a NumPy dtype. Check if it's a categorical maybe
            if isinstance(dtype, pd.CategoricalDtype):
                kind = 23
            else:
                raise ValueError(f"Data type {dtype} not supported by exchange"
                                 "protocol")

        if kind not in (_k.INT, _k.UINT, _k.FLOAT, _k.BOOL, _k.CATEGORICAL):
            raise NotImplementedError(f"Data type {dtype} not handled yet")

        bitwidth = dtype.itemsize * 8
        format_str = dtype.str
        endianness = dtype.byteorder if not kind == _k.CATEGORICAL else '='
        return (kind, bitwidth, format_str, endianness)


    @property
    def describe_categorical(self) -> Dict[str, Any]:
        """
        If the dtype is categorical, there are two options:

        - There are only values in the data buffer.
        - There is a separate dictionary-style encoding for categorical values.

        Raises RuntimeError if the dtype is not categorical

        Content of returned dict:

            - "is_ordered" : bool, whether the ordering of dictionary indices is
                             semantically meaningful.
            - "is_dictionary" : bool, whether a dictionary-style mapping of
                                categorical values to other objects exists
            - "mapping" : dict, Python-level only (e.g. ``{int: str}``).
                          None if not a dictionary-style categorical.

        TBD: are there any other in-memory representations that are needed?
        """
        raise NotImplementedError("TODO")

    @property
    def describe_null(self) -> Tuple[int, Any]:
        """
        Return the missing value (or "null") representation the column dtype
        uses, as a tuple ``(kind, value)``.

        Kind:

            - 0 : non-nullable
            - 1 : NaN/NaT
            - 2 : sentinel value
            - 3 : bit mask
            - 4 : byte mask

        Value : if kind is "sentinel value", the actual value. None otherwise.
        """
        _k = _DtypeKind
        kind = self.dtype[0]
        value = None
        if kind == _k.FLOAT:
            null = 1  # np.nan
        elif kind == _k.DATETIME:
            null = 1  # np.datetime64('NaT')
        elif kind in (_k.INT, _k.UINT, _k.BOOL):
            # TODO: check if extension dtypes are used once support for them is
            #       implemented in this procotol code
            null = 0  # integer and boolean dtypes are non-nullable
        elif kind == _k.CATEGORICAL:
            # Null values for categoricals are stored as `-1` sentinel values
            # in the category date (e.g., `col.values.codes` is int8 np.ndarray)
            null = 2
            value = -1
        else:
            raise NotImplementedError(f'Data type {self.dtype} not yet supported')

        return null, value

    @property
    def null_count(self) -> int:
        """
        Number of null elements. Should always be known.
        """
        return self._col.isna().sum()

    def num_chunks(self) -> int:
        """
        Return the number of chunks the column consists of.
        """
        return 1

    def get_chunks(self, n_chunks : Optional[int] = None) -> Iterable['_PandasColumn']:
        """
        Return an iterator yielding the chunks.

        See `DataFrame.get_chunks` for details on ``n_chunks``.
        """
        return (self,)

    def get_data_buffer(self) -> _PandasBuffer:
        """
        Return the buffer containing the data.
        """
        return _PandasBuffer(self._col.to_numpy())

    def get_mask(self) -> _PandasBuffer:
        """
        Return the buffer containing the mask values indicating missing data.

        Raises RuntimeError if null representation is not a bit or byte mask.
        """
        null = self.describe_null()
        if null == 0:
            msg = "This column is non-nullable so does not have a mask"
        elif null == 1:
            msg = "This column uses NaN as null so does not have a separate mask"
        else:
            raise NotImplementedError('See self.describe_null')

        raise RuntimeError(msg)


class _PandasDataFrame:
    """
    A data frame class, with only the methods required by the interchange
    protocol defined.

    Instances of this (private) class are returned from
    ``pd.DataFrame.__dataframe__`` as objects with the methods and
    attributes defined on this class.
    """
    def __init__(self, df : pd.DataFrame, nan_as_null : bool = False) -> None:
        """
        Constructor - an instance of this (private) class is returned from
        `pd.DataFrame.__dataframe__`.
        """
        self._df = df
        # ``nan_as_null`` is a keyword intended for the consumer to tell the
        # producer to overwrite null values in the data with ``NaN`` (or ``NaT``).
        # This currently has no effect; once support for nullable extension
        # dtypes is added, this value should be propagated to columns.
        self._nan_as_null = nan_as_null

    def num_columns(self) -> int:
        return len(self._df.columns)

    def num_rows(self) -> int:
        return len(self._df)

    def num_chunks(self) -> int:
        return 1

    def column_names(self) -> Iterable[str]:
        return self._df.columns.tolist()

    def get_column(self, i: int) -> _PandasColumn:
        return _PandasColumn(self._df.iloc[:, i])

    def get_column_by_name(self, name: str) -> _PandasColumn:
        return _PandasColumn(self._df[name])

    def get_columns(self) -> Iterable[_PandasColumn]:
        return [_PandasColumn(self._df[name]) for name in self._df.columns]

    def select_columns(self, indices: Sequence[int]) -> '_PandasDataFrame':
        if not isinstance(indices, collections.Sequence):
            raise ValueError("`indices` is not a sequence")

        return _PandasDataFrame(self._df.iloc[:, indices])

    def select_columns_by_name(self, names: Sequence[str]) -> '_PandasDataFrame':
        if not isinstance(names, collections.Sequence):
            raise ValueError("`names` is not a sequence")

        return _PandasDataFrame(self._df.xs(indices, axis='columns'))

    def get_chunks(self, n_chunks : Optional[int] = None) -> Iterable['_PandasDataFrame']:
        """
        Return an iterator yielding the chunks.
        """
        return (self,)


# Roundtrip testing
# -----------------

def test_float_only():
    df = pd.DataFrame(data=dict(a=[1.5, 2.5, 3.5], b=[9.2, 10.5, 11.8]))
    df2 = from_dataframe(df)
    tm.assert_frame_equal(df, df2)


def test_mixed_intfloat():
    df = pd.DataFrame(data=dict(a=[1, 2, 3], b=[3, 4, 5],
                                c=[1.5, 2.5, 3.5], d=[9, 10, 11]))
    df2 = from_dataframe(df)
    tm.assert_frame_equal(df, df2)


def test_noncontiguous_columns():
    # Currently raises: TBD whether it should work or not, see code comment
    # where the RuntimeError is raised.
    arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    df = pd.DataFrame(arr)
    assert df[0].to_numpy().strides == (24,)
    pytest.raises(RuntimeError, from_dataframe, df)
    #df2 = from_dataframe(df)


def test_categorical_dtype():
    df = pd.DataFrame({"A": [1, 2, 3, 1]})
    df["B"] = df["A"].astype("category")
    df.at[1, 'B'] = np.nan  # Set one item to null
    df2 = from_dataframe(df)


if __name__ == '__main__':
    test_float_only()
    test_mixed_intfloat()
    test_noncontiguous_columns()
    test_categorical_dtype()

