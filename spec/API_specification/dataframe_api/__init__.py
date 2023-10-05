"""
Function stubs and API documentation for the DataFrame API standard.
"""
from __future__ import annotations

from typing import Mapping, Sequence, Any, Literal, TYPE_CHECKING

from .permissivecolumn_object import PermissiveColumn
from .permissiveframe_object import PermissiveFrame
from .column_object import Column
from .dataframe_object import DataFrame
from .groupby_object import *
from .dtypes import *

if TYPE_CHECKING:
    from ._types import DType

__all__ = [
    "__dataframe_api_version__",
    "DataFrame",
    "PermissiveFrame",
    "PermissiveColumn",
    "Column",
    "GroupBy",
    "column_from_sequence",
    "column_from_1d_array",
    "col",
    "concat",
    "dataframe_from_dict",
    "sorted_indices",
    "unique_indices",
    "dataframe_from_2d_array",
    "is_null",
    "null",
    "Int64",
    "Int32",
    "Int16",
    "Int8",
    "UInt64",
    "UInt32",
    "UInt16",
    "UInt8",
    "Float64",
    "Float32",
    "Bool",
    "Date",
    "Datetime",
    "Duration",
    "String",
    "is_dtype",
    "any_rowwise",
    "all_rowwise",
]


__dataframe_api_version__: str = "YYYY.MM"
"""
String representing the version of the DataFrame API specification to which
the conforming implementation adheres. Set to a concrete value for a stable
implementation of the dataframe API standard.
"""

def col(name: str) -> Column:
    """
    Instantiate an Column which selects given column by name.

    For example, to select column 'species' and then use it to filter
    a DataFrame, you could do:

    .. code-block::python

        df: DataFrame
        namespace = df.__dataframe_namespace__()
        df.filter(namespace.col('species') == 'setosa')
    """
    ...

def concat(dataframes: Sequence[DataFrame]) -> DataFrame:
    """
    Concatenate DataFrames vertically.

    To concatenate horizontally, please use ``insert``.

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

def column_from_sequence(sequence: Sequence[Any], *, dtype: DType, name: str = '') -> PermissiveColumn:
    """
    Construct PermissiveColumn from sequence of elements.

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
    PermissiveColumn
    """
    ...

def dataframe_from_dict(data: Mapping[str, PermissiveColumn]) -> DataFrame:
    """
    Construct DataFrame from map of column names to PermissiveColumns.

    Parameters
    ----------
    data : Mapping[str, PermissiveColumn]
        PermissiveColumn must be of the corresponding type of the DataFrame.
        For example, it is only supported to build a ``LibraryXDataFrame`` using
        ``LibraryXColumn`` instances.

    Returns
    -------
    DataFrame
    
    Raises
    ------
    ValueError
        If any of the columns already has a name, and the corresponding key
        in `data` doesn't match.

    """
    ...


def column_from_1d_array(array: Any, *, dtype: DType, name: str = '') -> PermissiveColumn:
    """
    Construct PermissiveColumn from 1D array.

    See `dataframe_from_2d_array` for related 2D function.

    Only Array-API-compliant 1D arrays are supported.
    Cross-kind casting is undefined and may vary across implementations.
    Downcasting is disallowed.

    Parameters
    ----------
    array : array
        array-API compliant 1D array
    name : str, optional
        Name to give columns.
    dtype : DType
        Dtype of column.

    Returns
    -------
    PermissiveColumn
    """
    ...

def dataframe_from_2d_array(array: Any, *, names: Sequence[str], dtypes: Mapping[str, Any]) -> DataFrame:
    """
    Construct DataFrame from 2D array.

    See `column_from_1d_array` for related 1D function.

    Only Array-API-compliant 2D arrays are supported.
    Cross-kind casting is undefined and may vary across implementations.
    Downcasting is disallowed.

    Parameters
    ----------
    array : array
        array-API compliant 2D array
    names : Sequence[str]
        Names to give columns. Must be the same length as ``array.shape[1]``.
    dtypes : Mapping[str, DType]
        Dtype of each column. Must be the same length as ``array.shape[1]``.

    Returns
    -------
    DataFrame
    """
    ...

def any_rowwise(*columns: str | Column | PermissiveColumn, skip_nulls: bool = True) -> Column:
    """
    Reduction returns an Column.

    Differs from ``DataFrame.any`` and that the reduction happens
    for each row, rather than for each column.

    Parameters
    ----------
    columns : str | Column | PermissiveColumn
        Columns to consider.

    Raises
    ------
    ValueError
        If any of the DataFrame's columns is not boolean.
    """
    ...

def all_rowwise(*columns: str | Column | PermissiveColumn, skip_nulls: bool = True) -> Column:
    """
    Reduction returns an Column.

    Differs from ``DataFrame.all`` and that the reduction happens
    for each row, rather than for each column.

    Parameters
    ----------
    columns : str | Column | PermissiveColumn
        Columns to consider.

    Raises
    ------
    ValueError
        If any of the DataFrame's columns is not boolean.
    """
    ...

def sorted_indices(
    *columns: str | Column | PermissiveColumn,
    ascending: Sequence[bool] | bool = True,
    nulls_position: Literal['first', 'last'] = 'last',
) -> Column:
    """
    Return row numbers which would sort according to given columns.

    If you need to sort the DataFrame, use :meth:`DataFrame.sort`.

    Parameters
    ----------
    columns : str | Column | PermissiveColumn
        Column(s) to sort by.
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

    Raises
    ------
    ValueError
        If `keys` and `ascending` are sequences of different lengths.
    """
    ...


def unique_indices(
        *columns: str | Column | PermissiveColumn,
        skip_nulls: bool = True,
    ) -> Column:
    """
    Return indices corresponding to unique values across selected columns.

    Parameters
    ----------
    columns : str | Column | PermissiveColumn
        Columns to consider when finding unique values.

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
    """
    ...



class null:
    """
    A `null` object to represent missing data.

    ``null`` is a scalar, and may be used when constructing a  `PermissiveColumn` from a
    Python sequence with `column_from_sequence`. It does not support ``is``,
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
    ...

def is_null(value: object, /) -> bool:
    """
    Check if an object is a `null` scalar.

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

def is_dtype(dtype: DType, kind: str | tuple[str, ...]) -> bool:
    """
    Returns a boolean indicating whether a provided dtype is of a specified data type “kind”.

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
            - 'unsigned integer': unsigned integer data types (UInt8, UInt16, UInt32, UInt64).
            - 'floating': floating-point data types (Float32, Float64).
            - 'integral': integer data types. Shorthand for ('signed integer', 'unsigned integer').
            - 'numeric': numeric data types. Shorthand for ('integral', 'floating').

            If kind is a tuple, the tuple specifies a union of dtypes and/or kinds,
            and the function must return a boolean indicating whether the input dtype
            is either equal to a specified dtype or belongs to at least one specified
            data type kind.

    Returns
    -------
    bool
    """
