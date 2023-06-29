from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .dataframe_object import DataFrame


__all__ = ['GroupBy']


class GroupBy:
    """
    GroupBy object.

    Note that this class is not meant to be constructed by users.
    It is returned from `DataFrame.groupby`.

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

    def std(self, *, skip_nulls: bool = True) -> DataFrame:
        ...

    def var(self, *, skip_nulls: bool = True) -> DataFrame:
        ...

    def size(self) -> DataFrame:
        ...
