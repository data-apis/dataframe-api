from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dataframe_api.column_object import Column
    from dataframe_api.dataframe_object import DataFrame
    from dataframe_api.scalar_object import Scalar
    from dataframe_api.typing import SupportsDataFrameAPI


def main(df_raw: SupportsDataFrameAPI) -> SupportsDataFrameAPI:
    df = df_raw.__dataframe_consortium_standard__(api_version="2023-11.beta")

    # `DataFrame.fill_null` accepts `AnyScalar` objections.
    # This means we can fill nulls using a Standard Scalar object...
    df = df.fill_null(df.col("a").mean())

    # ... but also Python scalars:
    df = df.fill_null(3)
    df = df.fill_null("3")

    # Scalars can be used in arithmetic expressions with other scalars, columns,
    # or DataFrames
    value: Scalar = df.col("a").mean()
    col: Column = df.col("a")
    _res1: Column = value - col
    _res2: Scalar = value - 3
    _res3: Scalar = 3 - value
    _res4: Column = df.col("a") - 3
    _res5: DataFrame = df - value
    _res6: DataFrame = value - df

    return df.dataframe
