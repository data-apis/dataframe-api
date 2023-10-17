from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from dataframe_api.typing import DataFrame, SupportsDataFrameAPI


def query(
    customer_raw: SupportsDataFrameAPI,
    orders_raw: SupportsDataFrameAPI,
    lineitem_raw: SupportsDataFrameAPI,
    supplier_raw: SupportsDataFrameAPI,
    nation_raw: SupportsDataFrameAPI,
    region_raw: SupportsDataFrameAPI,
) -> Any:
    customer = customer_raw.__dataframe_consortium_standard__()
    orders = orders_raw.__dataframe_consortium_standard__()
    lineitem = lineitem_raw.__dataframe_consortium_standard__()
    supplier = supplier_raw.__dataframe_consortium_standard__()
    nation = nation_raw.__dataframe_consortium_standard__()
    region = region_raw.__dataframe_consortium_standard__()

    namespace = customer.__dataframe_namespace__()

    result = (
        region.join(nation, how="inner", left_on="r_regionkey", right_on="n_regionkey")
        .join(customer, how="inner", left_on="n_nationkey", right_on="c_nationkey")
        .join(orders, how="inner", left_on="c_custkey", right_on="o_custkey")
        .join(lineitem, how="inner", left_on="o_orderkey", right_on="l_orderkey")
        .join(
            supplier,
            how="inner",
            left_on=["l_suppkey", "n_nationkey"],
            right_on=["s_suppkey", "s_nationkey"],
        )
    )
    mask = (
        (
            result.get_column_by_name("c_nationkey")
            == result.get_column_by_name("s_nationkey")
        )
        & (result.get_column_by_name("r_name") == "ASIA")
        & (result.get_column_by_name("o_orderdate") >= namespace.date(1994, 1, 1))  # type: ignore
        & (result.get_column_by_name("o_orderdate") < namespace.date(1995, 1, 1))  # type: ignore
    )
    result = result.filter(mask)

    new_column = (
        result.get_column_by_name("l_extendedprice")
        * (result.get_column_by_name("l_discount") * -1 + 1)
    ).rename("revenue")
    result = result.assign(new_column)
    result = result.select(["revenue", "n_name"])
    result = result.group_by("n_name").sum()

    return result.dataframe
