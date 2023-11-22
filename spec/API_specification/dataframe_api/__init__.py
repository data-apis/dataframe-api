# mypy: disable-error-code="empty-body"
"""Function stubs and API documentation for the DataFrame API standard."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from .column_object import Column
from .dataframe_object import DataFrame
from .dtypes import (
    Bool,
    Date,
    Datetime,
    Duration,
    Float32,
    Float64,
    Int8,
    Int16,
    Int32,
    Int64,
    String,
    UInt8,
    UInt16,
    UInt32,
    UInt64,
)
from .groupby_object import Aggregation, GroupBy

if TYPE_CHECKING:
    from collections.abc import Sequence

    from .typing import DType, Scalar

__all__ = [
    "GroupBy",
    "Aggregation",
    "Bool",
    "Date",
    "Datetime",
    "Duration",
    "Float32",
    "Float64",
    "Int16",
    "Int32",
    "Int64",
    "Int8",
    "String",
    "UInt16",
    "UInt32",
    "UInt64",
    "UInt8",
    "Column",
    "DataFrame",
    "__dataframe_api_version__",
    "column_from_1d_array",
    "column_from_sequence",
    "concat",
    "dataframe_from_2d_array",
    "dataframe_from_columns",
    "date",
    "is_dtype",
    "is_null",
    "null",
]


__dataframe_api_version__: str = "YYYY.MM"
"""
String representing the version of the DataFrame API specification to which
the conforming implementation adheres. Set to a concrete value for a stable
implementation of the dataframe API standard.
"""


def concat(dataframes: Sequence[DataFrame]) -> DataFrame:
    """Concatenate DataFrames vertically.

    Parameters
    ----------
    dataframes : Sequence[DataFrame]
        DataFrames to concatenate.
        Column names, ordering, and dtypes must match.

    Notes
    -----
    The order in which the input DataFrames appear in
    the output is preserved (so long as the DataFrame implementation supports row
    ordering).
    """
    ...


def column_from_sequence(
    sequence: Sequence[Any],
    *,
    dtype: DType,
    name: str = "",
) -> Column:
    """Construct Column from sequence of elements.

    Parameters
    ----------
    sequence : Sequence[object]
        Sequence of elements. Each element must be of the specified
        ``dtype``, the corresponding Python builtin scalar type, or
        coercible to that Python scalar type.
    name : str, optional
        Name of column.
    dtype : DType
        Dtype of result. Must be specified.

    Returns
    -------
    Column
    """
    ...


def dataframe_from_columns(*columns: Column) -> DataFrame:
    """Construct DataFrame from sequence of Columns.

    Parameters
    ----------
    columns : Column
        Column(s) must be of the corresponding type of the DataFrame.
        For example, it is only supported to build a ``LibraryXDataFrame`` using
        ``LibraryXColumn`` instances.

    Returns
    -------
    DataFrame
    """
    ...


def column_from_1d_array(array: Any, *, name: str = "") -> Column:
    """Construct Column from 1D array.

    See `dataframe_from_2d_array` for related 2D function.

    Only Array-API-compliant 1D arrays are supported.

    The resulting column will have the dtype corresponding to the
    Array API one:

    -  'bool' -> Bool()
    -  'int8' -> Int8()
    -  'int16' -> Int16()
    -  'int32' -> Int32()
    -  'int64' -> Int64()
    -  'uint8' -> UInt8()
    -  'uint16' -> UInt16()
    -  'uint32' -> UInt32()
    -  'uint64' -> UInt64()
    -  'float32' -> Float32()
    -  'float64' -> Float64()

    Parameters
    ----------
    array : array
        array-API compliant 1D array
    name : str, optional
        Name to give columns.

    Returns
    -------
    Column
    """
    ...


def dataframe_from_2d_array(array: Any, *, names: Sequence[str]) -> DataFrame:
    """Construct DataFrame from 2D array.

    See `column_from_1d_array` for related 1D function.

    Only Array-API-compliant 2D arrays are supported.

    The resulting columns will have the dtype corresponding to the
    Array API one:

    -  'bool' -> Bool()
    -  'int8' -> Int8()
    -  'int16' -> Int16()
    -  'int32' -> Int32()
    -  'int64' -> Int64()
    -  'uint8' -> UInt8()
    -  'uint16' -> UInt16()
    -  'uint32' -> UInt32()
    -  'uint64' -> UInt64()
    -  'float32' -> Float32()
    -  'float64' -> Float64()

    Parameters
    ----------
    array : array
        array-API compliant 2D array
    names : Sequence[str]
        Names to give columns.

    Returns
    -------
    DataFrame
    """
    ...


class null:  # noqa: N801
    """A `null` object to represent missing data.

    Not meant to be instantiated, use ``null`` directly.

    ``null`` is a scalar, and may be used when constructing a `Column` from a
    Python sequence with :func:`column_from_sequence`. It does not support ``is``,
    ``==`` or ``bool``.

    Raises
    ------
    TypeError
        From ``__eq__`` and from ``__bool__``.

        For ``__eq__``: a missing value must not be compared for equality
        directly. Instead, use `DataFrame.is_null` or `Column.is_null` to check
        for presence of missing values.

        For ``__bool__``: truthiness of a missing value is ambiguous.

    Notes
    -----
    Like for Python scalars, the ``null`` object may be duck typed so it can
    reside on (e.g.) a GPU. Hence, the builtin ``is`` keyword should not be
    used to check if an object *is* the ``null`` object.

    """


def is_null(value: object, /) -> bool:
    """Check if an object is a `null` scalar.

    Parameters
    ----------
    value : object
        Any input type is valid.

    Returns
    -------
    bool
        True if the input is a `null` object from the same library which
        implements the dataframe API standard, False otherwise.
    """
    ...


def is_dtype(dtype: DType, kind: str | tuple[str, ...]) -> bool:
    """Indicate whether a provided dtype is of a specified data type "kind".

    Parameters
    ----------
        dtype: DType
            The input dtype.
        kind: str
            data type kind.
            The function must return a boolean indicating whether
            the input dtype is of a specified data type kind.
            The following dtype kinds must be supported:

            - 'bool': boolean data type (Bool).
            - 'signed integer': signed integer data types (Int8, Int16, Int32, Int64).
            - 'unsigned integer': unsigned integer data types
              (UInt8, UInt16, UInt32, UInt64).
            - 'floating': floating-point data types (Float32, Float64).
            - 'integral': integer data types. Shorthand for
              ('signed integer', 'unsigned integer').
            - 'numeric': numeric data types. Shorthand for ('integral', 'floating').

            If kind is a tuple, the tuple specifies a union of dtypes and/or kinds,
            and the function must return a boolean indicating whether the input dtype
            is either equal to a specified dtype or belongs to at least one specified
            data type kind.

    Returns
    -------
    bool
    """
    ...


def date(year: int, month: int, day: int) -> Scalar:
    """Create date object which can be used for filtering.

    The full 32-bit signed integer range of days since epoch should be supported
    (between -5877641-06-23 and 5881580-07-11 inclusive).

    Examples
    --------
    >>> df: DataFrame
    >>> pdx = df.__dataframe_namespace__()
    >>> mask = (
    ...     (df.get_column_by_name('date') >= pdx.date(2020, 1, 1))
    ...     & (df.get_column_by_name('date') < pdx.date(2021, 1, 1))
    ... )
    >>> df.filter(mask)
    """


def any_horizontal(*columns: Column, skip_nulls: bool = True) -> Column:
    """Reduction returns a Column.

    Differs from :meth:`DataFrame.any` in that the reduction happens
    for each row, rather than for each column.

    All the `columns` must have the same parent DataFrame.
    The return value has the same parent DataFrame as the input columns.

    Raises
    ------
    ValueError
        If any of the columns is not boolean.

    Examples
    --------
    >>> df: DataFrame
    >>> pdx = df.__dataframe_namespace__()
    >>> mask = pdx.any_horizontal(
    ...     *[df.col(col_name) > 0 for col_name in df.column_names()]
    ... )
    >>> df = df.filter(mask)
    """
    ...


def all_horizontal(*columns: Column, skip_nulls: bool = True) -> Column:
    """Reduction returns a Column.

    Differs from :meth:`DataFrame.all` in that the reduction happens
    for each row, rather than for each column.

    All the `columns` must have the same parent DataFrame.
    The return value has the same parent DataFrame as the input columns.

    Raises
    ------
    ValueError
        If any of the columns is not boolean.

    Examples
    --------
    >>> df: DataFrame
    >>> pdx = df.__dataframe_namespace__()
    >>> mask = pdx.all_horizontal(
    ...     *[df.col(col_name) > 0 for col_name in df.column_names()]
    ... )
    >>> df = df.filter(mask)
    """
    ...


def sorted_indices(
    *columns: Column,
    ascending: Sequence[bool] | bool = True,
    nulls_position: Literal["first", "last"] = "last",
) -> Column:
    """Return row numbers which would sort according to given columns.

    If you need to sort the DataFrame, use :meth:`sort`.

    Parameters
    ----------
    *columns : Column
        Columns to sort by.
    ascending : Sequence[bool] or bool
        If `True`, sort by all keys in ascending order.
        If `False`, sort by all keys in descending order.
        If a sequence, it must be the same length as `keys`,
        and determines the direction with which to use each
        key to sort by.
    nulls_position : ``{'first', 'last'}``
        Whether null values should be placed at the beginning
        or at the end of the result.
        Note that the position of NaNs is unspecified and may
        vary based on the implementation.

    Returns
    -------
    Column
        The return value has the same parent DataFrame as the input columns.

    Raises
    ------
    ValueError
        If `keys` and `ascending` are sequences of different lengths.
    """
    ...


def unique_indices(*columns: Column, skip_nulls: bool = True) -> Column:
    """Return indices corresponding to unique values across selected columns.

    Parameters
    ----------
    *columns : Column
        Column names to consider when finding unique values.

    Returns
    -------
    Column
        Indices corresponding to unique values.

    Notes
    -----
    There are no ordering guarantees. In particular, if there are multiple
    indices corresponding to the same unique value(s), there is no guarantee
    about which one will appear in the result.
    If the original column(s) contain multiple `'NaN'` values, then
    only a single index corresponding to those values will be returned.
    Likewise for null values (if ``skip_nulls=False``).
    To get the unique values, you can do ``df.get_rows(df.unique_indices(keys))``.
    """
    ...
