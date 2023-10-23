"""
Original query:

SELECT n_name, SUM(l_extendedprice * (1 - l_discount)) AS revenue
  FROM customer, orders, lineitem, supplier, nation, region
 WHERE c_custkey = o_custkey
   AND l_orderkey = o_orderkey
   AND l_suppkey = s_suppkey
   AND c_nationkey = s_nationkey
   AND s_nationkey = n_nationkey
   AND n_regionkey = r_regionkey
   AND r_name = 'ASIA'
   AND o_orderdate >= MDY(1,1,1994)
   AND o_orderdate < MDY(1,1,1994) + 1 UNITS YEAR
GROUP BY n_name
ORDER BY revenue DESC
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dataframe_api.typing import SupportsDataFrameAPI


def query(
    customer_raw: SupportsDataFrameAPI,
    orders_raw: SupportsDataFrameAPI,
    lineitem_raw: SupportsDataFrameAPI,
    supplier_raw: SupportsDataFrameAPI,
    nation_raw: SupportsDataFrameAPI,
    region_raw: SupportsDataFrameAPI,
) -> SupportsDataFrameAPI:
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
        * (1 - result.get_column_by_name("l_discount"))
    ).rename("revenue")
    result = result.assign(new_column)
    result = result.group_by("n_name").aggregate(namespace.Aggregation.sum("revenue"))

    return result.dataframe
