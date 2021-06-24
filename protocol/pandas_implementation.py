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
import pandas.testing as tm
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
    _k = _DtypeKind
    for name in df.column_names():
        col = df.get_column_by_name(name)
        if col.dtype[0] in (_k.INT, _k.UINT, _k.FLOAT, _k.BOOL):
            # Simple numerical or bool dtype, turn into numpy array
            columns[name] = convert_column_to_ndarray(col)
        elif col.dtype[0] == _k.CATEGORICAL:
            columns[name] = convert_categorical_column(col)
        elif col.dtype[0] == _k.STRING:
            columns[name] = convert_string_column(col)
        else:
            raise NotImplementedError(f"Data type {col.dtype[0]} not handled yet")

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
    Convert an int, uint, float or bool column to a numpy array.
    """
    if col.offset != 0:
        raise NotImplementedError("column.offset > 0 not handled yet")

    if col.describe_null[0] not in (0, 1):
        raise NotImplementedError("Null values represented as masks or "
                                  "sentinel values not handled yet")

    _buffer, _dtype = col.get_data_buffer()
    return buffer_to_ndarray(_buffer, _dtype)


def buffer_to_ndarray(_buffer, _dtype) -> np.ndarray:
    # Handle the dtype
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
    ctypes_type = np.ctypeslib.as_ctypes_type(column_dtype)
    data_pointer = ctypes.cast(_buffer.ptr, ctypes.POINTER(ctypes_type))

    # NOTE: `x` does not own its memory, so the caller of this function must
    #       either make a copy or hold on to a reference of the column or
    #       buffer! (not done yet, this is pretty awful ...)
    x = np.ctypeslib.as_array(data_pointer,
                              shape=(_buffer.bufsize // (bitwidth//8),))

    return x


def convert_categorical_column(col : ColumnObject) -> pd.Series:
    """
    Convert a categorical column to a Series instance.
    """
    ordered, is_dict, mapping = col.describe_categorical
    if not is_dict:
        raise NotImplementedError('Non-dictionary categoricals not supported yet')

    # If you want to cheat for testing (can't use `_col` in real-world code):
    #    categories = col._col.values.categories.values
    #    codes = col._col.values.codes
    categories = np.asarray(list(mapping.values()))
    codes_buffer, codes_dtype = col.get_data_buffer()
    codes = buffer_to_ndarray(codes_buffer, codes_dtype)
    values = categories[codes]

    # Seems like Pandas can only construct with non-null values, so need to
    # null out the nulls later
    cat = pd.Categorical(values, categories=categories, ordered=ordered)
    series = pd.Series(cat)
    null_kind = col.describe_null[0]
    if null_kind == 2:  # sentinel value
        sentinel = col.describe_null[1]
        series[codes == sentinel] = np.nan
    else:
        raise NotImplementedError("Only categorical columns with sentinel "
                                  "value supported at the moment")

    return series


def convert_string_column(col : ColumnObject) -> np.ndarray:
    """
    Convert a string column to a NumPy array.
    """
    # Retrieve the data buffer containing the UTF-8 code units
    dbuffer, bdtype = col.get_data_buffer()

    # Retrieve the offsets buffer containing the index offsets demarcating the beginning and end of each string
    obuffer, odtype = col.get_offsets()

    # Retrieve the mask buffer indicating the presence of missing values:
    mbuffer, mdtype = col.get_mask()

    # Convert the buffers to NumPy arrays
    dt = (_DtypeKind.UINT, 8, None, None)  # note: in order to go from STRING to an equivalent ndarray, we claim that the buffer is uint8 (i.e., a byte array)
    dbuf = buffer_to_ndarray(dbuffer, dt)

    obuf = buffer_to_ndarray(obuffer, odtype)
    mbuf = buffer_to_ndarray(mbuffer, mdtype)

    # Assemble the strings from the code units
    str_list = []
    for i in range(obuf.size-1):
        # Check for missing values
        if mbuf[i] == 0:  # FIXME: we need to account for a mask buffer which is a bit array
            str_list.append(np.nan)
            continue

        # Extract a range of code units
        units = dbuf[obuf[i]:obuf[i+1]];

        # Convert the list of code units to bytes: 
        b = bytes(units)

        # Create the string
        s = b.decode(encoding="utf-8")

        # Add to our list of strings:
        str_list.append(s)

    # Convert the string list to a NumPy array
    return np.asarray(str_list, dtype="object")


def __dataframe__(cls, nan_as_null : bool = False) -> dict:
    """
    The public method to attach to pd.DataFrame.

    We'll attach it via monkey-patching here for demo purposes. If Pandas adopts
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
        Buffer size in bytes.
        """
        return self._x.size * self._x.dtype.itemsize

    @property
    def ptr(self) -> int:
        """
        Pointer to start of the buffer as an integer.
        """
        return self._x.__array_interface__['data'][0]

    def __dlpack__(self):
        """
        DLPack not implemented in NumPy yet, so leave it out here.
        """
        raise NotImplementedError("__dlpack__")

    def __dlpack_device__(self) -> Tuple[enum.IntEnum, int]:
        """
        Device type and device ID for where the data in the buffer resides.
        """
        class Device(enum.IntEnum):
            CPU = 1

        return (Device.CPU, None)

    def __repr__(self) -> str:
        return 'PandasBuffer(' + str({'bufsize': self.bufsize,
                                      'ptr': self.ptr,
                                      'device': self.__dlpack_device__()[0].name}
                                      ) + ')'

class _PandasColumn:
    """
    A column object, with only the methods and properties required by the
    interchange protocol defined.

    A column can contain one or more chunks. Each chunk can contain up to three
    buffers - a data buffer, a mask buffer (depending on null representation),
    and an offsets buffer (if variable-size binary; e.g., variable-length
    strings).

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

        # For now, assume that, if the column dtype is 'O' (i.e., `object`), then we have an array of strings
        if not isinstance(dtype, pd.CategoricalDtype) and dtype.kind == 'O':
            return (_DtypeKind.STRING, 8, '=U1', '=')

        return self._dtype_from_pandasdtype(dtype)

    def _dtype_from_pandasdtype(self, dtype) -> Tuple[enum.IntEnum, int, str, str]:
        """
        See `self.dtype` for details.
        """
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

        if kind not in (_k.INT, _k.UINT, _k.FLOAT, _k.BOOL, _k.CATEGORICAL, _k.STRING):
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
        """
        if not self.dtype[0] == _DtypeKind.CATEGORICAL:
            raise TypeError("`describe_categorical only works on a column with "
                            "categorical dtype!")

        ordered = self._col.dtype.ordered
        is_dictionary = True
        # NOTE: this shows the children approach is better, transforming
        # `categories` to a "mapping" dict is inefficient
        codes = self._col.values.codes  # ndarray, length `self.size`
        # categories.values is ndarray of length n_categories
        categories = self._col.values.categories.values
        mapping = {ix: val for ix, val in enumerate(categories)}
        return ordered, is_dictionary, mapping

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
            #       implemented in this protocol code
            null = 0  # integer and boolean dtypes are non-nullable
        elif kind == _k.CATEGORICAL:
            # Null values for categoricals are stored as `-1` sentinel values
            # in the category date (e.g., `col.values.codes` is int8 np.ndarray)
            null = 2
            value = -1
        elif kind == _k.STRING:
            # For Pandas string extension dtype, use of `np.nan` for missing values may change!
            null = 1  # np.nan
        else:
            raise NotImplementedError(f"Data type {self.dtype} not yet supported")

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

    def get_data_buffer(self) -> Tuple[_PandasBuffer, Any]:  # Any is for self.dtype tuple
        """
        Return the buffer containing the data and the buffer's associated dtype.
        """
        _k = _DtypeKind
        if self.dtype[0] in (_k.INT, _k.UINT, _k.FLOAT, _k.BOOL):
            buffer = _PandasBuffer(self._col.to_numpy())
            dtype = self.dtype
        elif self.dtype[0] == _k.CATEGORICAL:
            codes = self._col.values.codes
            buffer = _PandasBuffer(codes)
            dtype = self._dtype_from_pandasdtype(codes.dtype)
        elif self.dtype[0] == _k.STRING:
            # Marshal the strings from a NumPy object array into a byte array
            buf = self._col.to_numpy()
            b = bytearray()
            for i in range(buf.size):
                if type(buf[i]) == str:
                    b.extend(buf[i].encode(encoding="utf-8"))

            # Convert the byte array to a Pandas "buffer" using a NumPy array as the backing store
            buffer = _PandasBuffer(np.frombuffer(b, dtype="uint8"))

            # Define the dtype for the returned buffer
            dtype = (_k.STRING, 8, "=U1", "=")  # note: currently only support native endianness
        else:
            raise NotImplementedError(f"Data type {self._col.dtype} not handled yet")

        return buffer, dtype

    def get_mask(self) -> Tuple[_PandasBuffer, Any]:
        """
        Return the buffer containing the mask values indicating missing data and
        the buffer's associated dtype.

        Raises RuntimeError if null representation is not a bit or byte mask.
        """
        _k = _DtypeKind
        if self.dtype[0] == _k.STRING:
            # For now, have the mask array be comprised of bytes, rather than a bit array
            buf = self._col.to_numpy()
            mask = []
            for i in range(buf.size):
                v = 0;
                if type(buf[i]) == str:
                    v += 1;  # follows Arrow where a valid value is 1 and null is 0

                mask.append(v)

            # Convert the mask array to a Pandas "buffer" using a NumPy array as the backing store
            buffer = _PandasBuffer(np.asarray(mask, dtype="uint8"))

            # Define the dtype of the returned buffer
            dtype = (_k.UINT, 8, "=B", "=")

            return buffer, dtype

        null, value = self.describe_null
        if null == 0:
            msg = "This column is non-nullable so does not have a mask"
        elif null == 1:
            msg = "This column uses NaN as null so does not have a separate mask"
        else:
            raise NotImplementedError("See self.describe_null")

        raise RuntimeError(msg)

    def get_offsets(self) -> Tuple[_PandasBuffer, Any]:
        """
        Return the buffer containing the offset values for variable-size binary
        data (e.g., variable-length strings) and the buffer's associated dtype.

        Raises RuntimeError if the data buffer does not have an associated
        offsets buffer.
        """
        _k = _DtypeKind
        if self.dtype[0] == _k.STRING:
            # For each string, we need to manually determine the next offset
            values = self._col.to_numpy()
            ptr = 0
            offsets = [ptr]
            for v in values:
                # For missing values (in this case, `np.nan` values), we don't increment the pointer)
                if type(v) == str:
                    b = v.encode(encoding="utf-8")
                    ptr += len(b)

                offsets.append(ptr)

            # Convert the list of offsets to a NumPy array of signed 64-bit integers (note: Arrow allows the offsets array to be either `int32` or `int64`; here, we default to the latter)
            buf = np.asarray(offsets, dtype="int64")

            # Convert the offsets to a Pandas "buffer" using the NumPy array as the backing store
            buffer = _PandasBuffer(buf)

            # Assemble the buffer dtype info
            bdtype = buf.dtype;
            dtype = (_k.INT, bdtype.itemsize*8, bdtype.str, "=")  # note: currently only support native endianness
        else:
            raise RuntimeError("This column has a fixed-length dtype so does not have an offsets buffer")

        return buffer, dtype


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
    df = pd.DataFrame({"A": [1, 2, 5, 1]})
    df["B"] = df["A"].astype("category")
    df.at[1, 'B'] = np.nan  # Set one item to null

    # Some detailed testing for correctness of dtype and null handling:
    col = df.__dataframe__().get_column_by_name('B')
    assert col.dtype[0] == _DtypeKind.CATEGORICAL
    assert col.null_count == 1
    assert col.describe_null == (2, -1)  # sentinel value -1
    assert col.num_chunks() == 1
    assert col.describe_categorical == (False, True, {0: 1, 1: 2, 2: 5})

    df2 = from_dataframe(df)
    tm.assert_frame_equal(df, df2)


def test_string_dtype():
    df = pd.DataFrame({"A": ["a", "b", "cdef", "", "g"]})
    df["B"] = df["A"].astype("object")
    df.at[1, "B"] = np.nan  # Set one item to null

    # Test for correctness and null handling:
    col = df.__dataframe__().get_column_by_name("B")
    assert col.dtype[0] == _DtypeKind.STRING
    assert col.null_count == 1
    assert col.describe_null == (1, None)
    assert col.num_chunks() == 1

    df2 = from_dataframe(df)
    tm.assert_frame_equal(df, df2)


if __name__ == '__main__':
    test_categorical_dtype()
    test_float_only()
    test_mixed_intfloat()
    test_noncontiguous_columns()
    test_string_dtype()

