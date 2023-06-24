from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Generic, Any

if TYPE_CHECKING:
    from .dataframe_object import DataFrame
    from . import IntDType, DType, Bool


__all__ = ['GroupBy']

T = TypeVar('T', bound="DType")


class GroupBy:
    """
    GroupBy object.

    Note that this class is not meant to be constructed by users.
    It is returned from `DataFrame.groupby`.

    **Methods**

    """
    def any(self, *, skip_nulls: bool = True) -> DataFrame[Bool]:
        ...

    def all(self, *, skip_nulls: bool = True) -> DataFrame[Bool]:
        ...

    def min(self, *, skip_nulls: bool = True) -> DataFrame[Any]:
        ...

    def max(self, *, skip_nulls: bool = True) -> DataFrame[Any]:
        ...

    def sum(self, *, skip_nulls: bool = True) -> DataFrame[Any]:
        ...

    def prod(self, *, skip_nulls: bool = True) -> DataFrame[Any]:
        ...

    def median(self, *, skip_nulls: bool = True) -> DataFrame[Any]:
        ...

    def mean(self, *, skip_nulls: bool = True) -> DataFrame[Any]:
        ...

    def std(self, *, skip_nulls: bool = True) -> DataFrame[Any]:
        ...

    def var(self, *, skip_nulls: bool = True) -> DataFrame[Any]:
        ...

    def size(self) -> DataFrame[IntDType]:
        ...
