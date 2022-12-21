from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .dataframe_object import DataFrame


class GroupBy:
    def any(self, skipna: bool = True) -> DataFrame:
        ...

    def all(self, skipna: bool = True) -> DataFrame:
        ...

    def min(self, skipna: bool = True) -> DataFrame:
        ...

    def max(self, skipna: bool = True) -> DataFrame:
        ...

    def sum(self, skipna: bool = True) -> DataFrame:
        ...

    def prod(self, skipna: bool = True) -> DataFrame:
        ...

    def median(self, skipna: bool = True) -> DataFrame:
        ...

    def mean(self, skipna: bool = True) -> DataFrame:
        ...

    def std(self, skipna: bool = True) -> DataFrame:
        ...

    def var(self, skipna: bool = True) -> DataFrame:
        ...
