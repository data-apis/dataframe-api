"""
Function stubs and API documentation for the DataFrame API standard.
"""
from __future__ import annotations

from typing import Mapping, Sequence

from .column_object import *
from .dataframe_object import *
from .groupby_object import *

from ._types import DType


__dataframe_api_version__: str = "YYYY.MM"
"""
String representing the version of the DataFrame API specification to which
the conforming implementation adheres. Set to a concrete value for a stable
implementation of the dataframe API standard.
"""

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

def column_from_sequence(sequence: Sequence[object], *, dtype: DType) -> Column:
    """
    Construct Column from sequence of elements.

    Parameters
    ----------
    sequence : Sequence[object]
        Sequence of elements. Each element must be of the specified
        ``dtype``, the corresponding Python builtin scalar type, or
        coercible to that Python scalar type.
    dtype : DType
        Dtype of result. Must be specified.

    Returns
    -------
    Column
    """
    ...

def dataframe_from_dict(data: Mapping[str, Column]) -> DataFrame:
    """
    Construct DataFrame from map of column names to Columns.

    Parameters
    ----------
    data : Mapping[str, Column]
        Column must be of the corresponding type of the DataFrame.
        For example, it is only supported to build a ``LibraryXDataFrame`` using
        ``LibraryXColumn`` instances.

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

        For ``_eq__``: a missing value must not be compared for equality
        directly. Instead, use `DataFrame.isnull` or `Column.isnull` to check
        for presence of missing values.

        For ``__bool__``: truthiness of a missing value is ambiguous.

    Notes
    -----
    Like for Python scalars, the ``null`` object may be duck typed so it can
    reside on (e.g.) a GPU. Hence, the builtin ``is`` keyword should not be
    used to check if an object *is* the ``null`` object.

    """
    ...
