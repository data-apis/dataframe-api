"""
Function stubs and API documentation for the DataFrame API standard.
"""
from typing import Sequence

from .column_object import *
from .dataframe_object import *
from .groupby_object import *


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
    the output is preserved.

    Returns
    -------
    DataFrame
    """
    ...
