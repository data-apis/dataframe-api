from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Callable

    from dataframe_api.typing import SupportsColumnAPI

my_plotting_function: Callable[[Any, Any], Any]


def group_by_and_plot(
    x_any: SupportsColumnAPI,
    y_any: SupportsColumnAPI,
    color_any: SupportsColumnAPI,
) -> None:
    x = x_any.__column_consortium_standard__(api_version="2023-10.beta")
    y = y_any.__column_consortium_standard__(api_version="2023-10.beta")
    color = color_any.__column_consortium_standard__(api_version="2023-10.beta")

    pdx = x.__column_namespace__()

    df = pdx.dataframe_from_columns(
        x.rename("x"),
        y.rename("y"),
        color.rename("color"),
    )

    agg = df.group_by("color").mean().fill_null(float("nan"))
    x = agg.col("x").to_array()
    y = agg.col("y").to_array()

    my_plotting_function(x, y)
