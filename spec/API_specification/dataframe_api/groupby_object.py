from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from .dataframe_object import DataFrame


__all__ = [
    "Aggregation",
    "GroupBy",
]


class GroupBy:
    """
    GroupBy object.

    Note that this class is not meant to be constructed by users.
    It is returned from `DataFrame.group_by`.

    **Methods**

    """
    def any(self, *, skip_nulls: bool = True) -> DataFrame:
        ...

    def all(self, *, skip_nulls: bool = True) -> DataFrame:
        ...

    def min(self, *, skip_nulls: bool = True) -> DataFrame:
        ...

    def max(self, *, skip_nulls: bool = True) -> DataFrame:
        ...

    def sum(self, *, skip_nulls: bool = True) -> DataFrame:
        ...

    def prod(self, *, skip_nulls: bool = True) -> DataFrame:
        ...

    def median(self, *, skip_nulls: bool = True) -> DataFrame:
        ...

    def mean(self, *, skip_nulls: bool = True) -> DataFrame:
        ...

    def std(self, *, correction: int | float = 1, skip_nulls: bool = True) -> DataFrame:
        ...

    def var(self, *, correction: int | float = 1, skip_nulls: bool = True) -> DataFrame:
        ...

    def size(self) -> DataFrame:
        ...

    def aggregate(self, *aggregation: Aggregation) -> DataFrame:
        """
        Aggregate columns according to given aggregation function.

        Examples
        --------
        >>> df: DataFrame
        >>> namespace = df.__dataframe_namespace__()
        >>> df.group_by('year').aggregate(
        ...     namespace.Aggregation.sum('l_quantity').rename('sum_qty'),
        ...     namespace.Aggregation.mean('l_quantity').rename('avg_qty'),
        ...     namespace.Aggregation.mean('l_extended_price').rename('avg_price'),
        ...     namespace.Aggregation.mean('l_discount').rename('avg_disc'),
        ...     namespace.Aggregation.size().rename('count_order'),
        ... )
        """
        ...

class Aggregation(Protocol):
    def rename(self, name: str) -> Aggregation:
        """Assign given name to output of aggregation. """
        ...

    @classmethod
    def any(cls, column: str, *, skip_nulls: bool = True) -> Aggregation:
        ...

    @classmethod
    def all(cls, column: str, *, skip_nulls: bool = True) -> Aggregation:
        ...

    @classmethod
    def min(cls, column: str, *, skip_nulls: bool = True) -> Aggregation:
        ...

    @classmethod
    def max(cls, column: str, *, skip_nulls: bool = True) -> Aggregation:
        ...

    @classmethod
    def sum(cls, column: str, *, skip_nulls: bool = True) -> Aggregation:
        ...

    @classmethod
    def prod(cls, column: str, *, skip_nulls: bool = True) -> Aggregation:
        ...

    @classmethod
    def median(cls, column: str, *, skip_nulls: bool = True) -> Aggregation:
        ...

    @classmethod
    def mean(cls, column: str, *, skip_nulls: bool=True) -> Aggregation:
        ...

    @classmethod
    def std(cls, column: str, *, correction: int|float=1, skip_nulls: bool=True) -> Aggregation:
        ...

    @classmethod
    def var(cls, column: str, *, correction: int|float=1, skip_nulls: bool=True) -> Aggregation:
        ...

    @classmethod
    def size(cls) -> Aggregation:
        ...

