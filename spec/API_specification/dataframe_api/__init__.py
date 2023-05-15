"""
Function stubs and API documentation for the DataFrame API standard.
"""
<<<<<<< HEAD
from typing import Sequence
=======
from __future__ import annotations

from typing import Mapping, Sequence
>>>>>>> upstream/main

from .column_object import *
from .dataframe_object import *
from .groupby_object import *

from ._types import dtype


__dataframe_api_version__: str = "YYYY.MM"
"""
String representing the version of the DataFrame API specification to which the
conforming implementation adheres.
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

def column_from_sequence(sequence: Sequence[object], *, dtype: dtype) -> Column:
    """
    Construct Column from sequence of elements.

    Parameters
    ----------
    sequence : Sequence[object]
        Sequence of elements. Each element must be of the specified
        ``dtype``, the corresponding Python builtin scalar type, or
        coercible to that Python scalar type.
    dtype : str
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
