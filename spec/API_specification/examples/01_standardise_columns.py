from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from dataframe_api.typing import SupportsDataFrameAPI


def my_dataframe_agnostic_function(df_non_standard: SupportsDataFrameAPI) -> Any:
    df = df_non_standard.__dataframe_consortium_standard__(api_version="2023.09-beta")

    new_columns = [
        ((col - col.mean()) / col.std()).rename(f"{col.name}_scaled")
        for col in df.columns_iter()
    ]
    df = df.assign(*new_columns)

    return df.dataframe
