"""
Function stubs and API documentation for the DataFrame API standard.
"""
from __future__ import annotations

from typing import Mapping, Sequence

from .column_object import *
from .dataframe_object import *
from .groupby_object import *

from ._types import dtype


__dataframe_api_version__: str = "YYYY.MM"
"""
String representing the version of the DataFrame API specification to which the
conforming implementation adheres.
"""

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
