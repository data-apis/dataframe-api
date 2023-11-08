"""Types for type annotations used in the dataframe API standard."""
from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    Protocol,
    Union,
)

from dataframe_api.column_object import Column
from dataframe_api.dataframe_object import DataFrame
from dataframe_api.groupby_object import Aggregation as AggregationT
from dataframe_api.groupby_object import GroupBy

from .scalar_object import Scalar

if TYPE_CHECKING:
    from collections.abc import Sequence

    from .dtypes import (
        Bool,
        Date,
        Datetime,
        Duration,
        Float32,
        Float64,
        Int8,
        Int16,
        Int32,
        Int64,
        String,
        UInt8,
        UInt16,
        UInt32,
        UInt64,
    )

    DType = Union[
        Bool,
        Float64,
        Float32,
        Int64,
        Int32,
        Int16,
        Int8,
        UInt64,
        UInt32,
        UInt16,
        UInt8,
        String,
        Date,
        Datetime,
        Duration,
    ]

# null is a special object which represents a missing value.
# It is not valid as a type.
NullType = Any


class Namespace(Protocol):
    __dataframe_api_version__: str

    class Int64:
        ...

    class Int32:
        ...

    class Int16:
        ...

    class Int8:
        ...

    class UInt64:
        ...

    class UInt32:
        ...

    class UInt16:
        ...

    class UInt8:
        ...

    class Float64:
        ...

    class Float32:
        ...

    class Bool:
        ...

    class Date:
        ...

    class Datetime:
        def __init__(  # noqa: ANN204
            self,
            time_unit: Literal["ms", "us"],
            time_zone: str | None,
        ):
            ...

    class String:
        ...

    Aggregation: AggregationT

    def concat(self, dataframes: Sequence[DataFrame]) -> DataFrame:
        ...

    def column_from_sequence(
        self,
        sequence: Sequence[Any],
        *,
        dtype: DType,
        name: str = "",
    ) -> Column:
        ...

    def dataframe_from_columns(self, *columns: Column) -> DataFrame:
        ...

    def column_from_1d_array(
        self,
        array: Any,
        *,
        dtype: DType,
        name: str = "",
    ) -> Column:
        ...

    def dataframe_from_2d_array(
        self,
        array: Any,
        *,
        schema: dict[str, DType],
    ) -> DataFrame:
        ...

    def is_null(self, value: object, /) -> bool:
        ...

    def is_dtype(self, dtype: DType, kind: str | tuple[str, ...]) -> bool:
        ...

    def date(self, year: int, month: int, day: int) -> Scalar:
        ...


class SupportsDataFrameAPI(Protocol):
    def __dataframe_consortium_standard__(
        self,
        *,
        api_version: str,
    ) -> DataFrame:
        ...


class SupportsColumnAPI(Protocol):
    def __column_consortium_standard__(
        self,
        *,
        api_version: str,
    ) -> Column:
        ...


__all__ = [
    "Column",
    "DataFrame",
    "DType",
    "GroupBy",
    "Namespace",
    "NullType",
    "Scalar",
    "SupportsColumnAPI",
    "SupportsDataFrameAPI",
]
