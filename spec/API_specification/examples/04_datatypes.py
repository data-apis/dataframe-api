from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from dataframe_api.typing import SupportsDataFrameAPI

some_array_function: Callable[[Any], Any]


def main(df_raw: SupportsDataFrameAPI) -> SupportsDataFrameAPI:
    df = df_raw.__dataframe_consortium_standard__(api_version="2023-11.beta").persist()
    pdx = df.__dataframe_namespace__()
    df = df.select(
        *[col.name for col in df.iter_columns() if isinstance(col.dtype, pdx.Int64)],
    )
    arr = df.to_array()
    arr = some_array_function(arr)
    df = pdx.dataframe_from_2d_array(arr, names=["a", "b"])
    return df.dataframe
