"""
Function stubs and API documentation for the DataFrame API standard.
"""
from __future__ import annotations

from typing import Mapping, Sequence, Any, Literal

from .expression_object import *
from .dataframe_object import DataFrame
from .groupby_object import *
from ._types import DType

__all__ = [
    "__dataframe_api_version__",
    "DataFrame",
    "col",
    "concat",
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
    "is_dtype",
]


__dataframe_api_version__: str = "YYYY.MM"
"""
String representing the version of the DataFrame API specification to which
the conforming implementation adheres. Set to a concrete value for a stable
implementation of the dataframe API standard.
"""

def col(name: str) -> Expression:
    """
    Instantiate an Expression which selects given column by name.

    For example, to select column 'species' and then use it to filter
    a DataFrame, you could do:

    .. code-block::python

        df: DataFrame
        namespace = df.__dataframe_namespace__()
        df.get_rows_by_mask(pl.col('species') == 'setosa')
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

def any_rowwise(keys: list[str] | None = None, *, skip_nulls: bool = True) -> Expression:
    """
    Reduction returns an Expression.

    Differs from ``DataFrame.any`` and that the reduction happens
    for each row, rather than for each column.

    Parameters
    ----------
    keys : list[str]
        Column names to consider. If `None`, all columns are considered.

    Raises
    ------
    ValueError
        If any of the DataFrame's columns is not boolean.
    """
    ...

def all_rowwise(keys: list[str] | None = None, *, skip_nulls: bool = True) -> Expression:
    """
    Reduction returns a Column.

    Differs from ``DataFrame.all`` and that the reduction happens
    for each row, rather than for each column.

    Parameters
    ----------
    keys : list[str]
        Column names to consider. If `None`, all columns are considered.

    Raises
    ------
    ValueError
        If any of the DataFrame's columns is not boolean.
    """
    ...

def sorted_indices(
    keys: str | list[str] | None = None,
    *,
    ascending: Sequence[bool] | bool = True,
    nulls_position: Literal['first', 'last'] = 'last',
) -> Expression:
    """
    Return row numbers which would sort according to given columns.

    If you need to sort the DataFrame, use :meth:`DataFrame.sort`.

    Parameters
    ----------
    keys : str | list[str], optional
        Names of columns to sort by.
        If `None`, sort by all columns.
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
    Expression

    Raises
    ------
    ValueError
        If `keys` and `ascending` are sequences of different lengths.
    """
    ...


def unique_indices(keys: str | list[str] | None = None, *, skip_nulls: bool = True) -> Expression:
    """
    Return indices corresponding to unique values across selected columns.

    Parameters
    ----------
    keys : str | list[str], optional
        Column names to consider when finding unique values.
        If `None`, all columns are considered.

    Returns
    -------
    Expression
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


def dataframe_from_2d_array(array: Any, *, names: Sequence[str], dtypes: Mapping[str, Any]) -> DataFrame:
    """
    Construct DataFrame from 2D array.

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
    api_version: str | None
        A string representing the version of the dataframe API specification
        in ``'YYYY.MM'`` form, for example, ``'2023.04'``.
        If it is ``None``, it should return an object corresponding to
        latest version of the dataframe API specification.  If the given
        version is invalid or not implemented for the given module, an
        error should be raised. Default: ``None``.

    Returns
    -------
    DataFrame
    """
    ...

class null:
    """
    A `null` object to represent missing data.

    ``null`` is a scalar, and may be used when constructing a `Column` from a
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

##########
# Dtypes #
##########

class Int64:
    """Integer type with 64 bits of precision."""

class Int32:
    """Integer type with 32 bits of precision."""

class Int16:
    """Integer type with 16 bits of precision."""

class Int8:
    """Integer type with 8 bits of precision."""

class UInt64:
    """Unsigned integer type with 64 bits of precision."""

class UInt32:
    """Unsigned integer type with 32 bits of precision."""

class UInt16:
    """Unsigned integer type with 16 bits of precision."""

class UInt8:
    """Unsigned integer type with 8 bits of precision."""

class Float64:
    """Floating point type with 64 bits of precision."""

class Float32:
    """Floating point type with 32 bits of precision."""

class Bool:
    """Boolean type with 8 bits of precision."""


def is_dtype(dtype: Any, kind: str | tuple[str, ...]) -> bool:
    """
    Returns a boolean indicating whether a provided dtype is of a specified data type “kind”.

    Parameters
    ----------
        dtype: Any
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
