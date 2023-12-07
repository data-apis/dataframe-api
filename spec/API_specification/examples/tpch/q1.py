from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from dataframe_api.typing import SupportsDataFrameAPI


def query(lineitem_raw: SupportsDataFrameAPI) -> Any:
    lineitem = lineitem_raw.__dataframe_consortium_standard__(api_version="2023.10-beta")
    pdx = lineitem.__dataframe_namespace__()

    mask = lineitem.col("l_shipdate") <= pdx.date(1998, 9, 2)
    lineitem = lineitem.assign(
        (lineitem.col("l_extended_price") * (1 - lineitem.col("l_discount"))).rename(
            "l_disc_price",
        ),
        (
            lineitem.col("l_extended_price")
            * (1 - lineitem.col("l_discount"))
            * (1 + lineitem.col("l_tax"))
        ).rename("l_charge"),
    )
    result = (
        lineitem.filter(mask)
        .group_by("l_returnflag", "l_linestatus")
        .aggregate(
            pdx.Aggregation.sum("l_quantity").rename("sum_qty"),
            pdx.Aggregation.sum("l_extendedprice").rename("sum_base_price"),
            pdx.Aggregation.sum("l_disc_price").rename("sum_disc_price"),
            pdx.Aggregation.sum("change").rename("sum_charge"),
            pdx.Aggregation.mean("l_quantity").rename("avg_qty"),
            pdx.Aggregation.mean("l_discount").rename("avg_disc"),
            pdx.Aggregation.size().rename("count_order"),
        )
        .sort("l_returnflag", "l_linestatus")
    )
    return result.dataframe
