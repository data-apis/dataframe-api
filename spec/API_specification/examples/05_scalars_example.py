from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dataframe_api.typing import SupportsDataFrameAPI


def main(df_raw: SupportsDataFrameAPI) -> SupportsDataFrameAPI:
    df = df_raw.__dataframe_consortium_standard__(api_version="2023-11.beta")

    # We can fill nulls using a Scalar object.
    df = df.fill_null(df.col("a").mean())

    # Python Scalars also implement the Scalar Protocol (indeed, the Scalar
    # Protocol is designed to be a subset of the Python Scalar types), so we
    # can pass Python scalars too.
    df = df.fill_null(3)
    return df.dataframe
