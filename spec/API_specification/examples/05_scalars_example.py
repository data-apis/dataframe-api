from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dataframe_api.typing import SupportsDataFrameAPI


def main(df_raw: SupportsDataFrameAPI) -> SupportsDataFrameAPI:
    df = df_raw.__dataframe_consortium_standard__(api_version="2023-11.beta")

    # `DataFrame.fill_null` accepts `AnyScalar` objections.
    # This means we can fill nulls using a Standard Scalar object...
    df = df.fill_null(df.col("a").mean())

    # ... but also Python scalars:
    df = df.fill_null(3)
    df = df.fill_null("3")
    return df.dataframe
