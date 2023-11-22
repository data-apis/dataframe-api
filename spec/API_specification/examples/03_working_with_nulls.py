"""Fill a column's NaN values with the implemenation's null value."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dataframe_api.typing import SupportsDataFrameAPI


def main(df_raw: SupportsDataFrameAPI) -> SupportsDataFrameAPI:
    df = df_raw.__dataframe_consortium_standard__(api_version="2023-11.beta")
    pdx = df.__dataframe_namespace__()
    df = df.fill_nan(pdx.null)
    return df.dataframe
