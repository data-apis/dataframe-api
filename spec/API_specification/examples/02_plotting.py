from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dataframe_api.typing import SupportsColumnAPI
    from typing import Callable, Any

my_plotting_function: Callable[[Any, Any], Any]


def group_by_and_plot(
    x_any: SupportsColumnAPI,
    y_any: SupportsColumnAPI,
    color_any: SupportsColumnAPI,
) -> None:
    x = x_any.__column_consortium_standard__()
    y = y_any.__column_consortium_standard__()
    color = color_any.__column_consortium_standard__()

    namespace = x.__column_namespace__()

    df = namespace.dataframe_from_dict({"x": x, "y": y, "color": color})

    agg = df.group_by("color").mean()
    x = agg.col("x").to_array_object(namespace.Float64())
    y = agg.col("y").to_array_object(namespace.Float64())

    my_plotting_function(x, y)
