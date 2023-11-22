"""Example of how to use a horizontal function.

Horizontal functions are functions that take multiple columns as input and return a
single column as output.

Examples include:
- `any_horizontal`
- `all_horizontal`

These can be accessed by first using ``__dataframe_namespace__`` to get the
namespace object, and then calling the function on the namespace object and passing
an iterable of ``Column``s as input.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dataframe_api.typing import SupportsDataFrameAPI


def main(df_raw: SupportsDataFrameAPI) -> SupportsDataFrameAPI:
    df = df_raw.__dataframe_consortium_standard__(api_version="2023-11.beta")
    pdx = df.__dataframe_namespace__()
    df = df.filter(
        pdx.any_horizontal(*[df.col(col_name) > 0 for col_name in df.column_names]),
    )
    return df.dataframe
