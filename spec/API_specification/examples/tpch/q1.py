from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from dataframe_api.typing import SupportsDataFrameAPI


def query(lineitem_raw: SupportsDataFrameAPI) -> Any:
    lineitem = lineitem_raw.__dataframe_consortium_standard__()
    namespace = lineitem.__dataframe_namespace__()

    mask = lineitem.get_column_by_name("l_shipdate") <= namespace.date(1998, 9, 2)
    lineitem = lineitem.assign(
        (
            lineitem.get_column_by_name("l_extended_price")
            * (1 - lineitem.get_column_by_name("l_discount"))
        ).rename("l_disc_price"),
        (
            lineitem.get_column_by_name("l_extended_price")
            * (1 - lineitem.get_column_by_name("l_discount"))
            * (1 + lineitem.get_column_by_name("l_tax"))
        ).rename("l_charge"),
    )
    result = (
        lineitem.filter(mask)
        .group_by("l_returnflag", "l_linestatus")
        .aggregate(
            namespace.Aggregation.sum("l_quantity").rename("sum_qty"),
            namespace.Aggregation.sum("l_extendedprice").rename("sum_base_price"),
            namespace.Aggregation.sum("l_disc_price").rename("sum_disc_price"),
            namespace.Aggregation.sum("change").rename("sum_charge"),
            namespace.Aggregation.mean("l_quantity").rename("avg_qty"),
            namespace.Aggregation.mean("l_discount").rename("avg_disc"),
            namespace.Aggregation.size().rename("count_order"),
        )
        .sort("l_returnflag", "l_linestatus")
    )
    return result.dataframe
