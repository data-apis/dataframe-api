"""
Types for type annotations used in the dataframe API standard.
"""
from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    Mapping,
    Protocol,
    Sequence,
    Union,
)

from dataframe_api.column_object import Column
from dataframe_api.dataframe_object import DataFrame
from dataframe_api.groupby_object import GroupBy, Aggregation as AggregationT

if TYPE_CHECKING:
    from .dtypes import (
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
        Date,
        Datetime,
        Duration,
        String,
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

# Type alias: Mypy needs Any, but for readability we need to make clear this
# is a Python scalar (i.e., an instance of `bool`, `int`, `float`, `str`, etc.)
Scalar = Any
# null is a special object which represents a missing value.
# It is not valid as a type.
NullType = Any


class Namespace(Protocol):
    __dataframe_api_version__: str

    class Int64():
        ...

    class Int32():
        ...

    class Int16():
        ...

    class Int8():
        ...

    class UInt64():
        ...

    class UInt32():
        ...

    class UInt16():
        ...

    class UInt8():
        ...

    class Float64():
        ...

    class Float32():
        ...

    class Bool():
        ...

    class Date():
        ...

    class Datetime():
        def __init__(
            self,
            time_unit: Literal['ms', 'us'],
            time_zone: str | None,
        ):
            ...

    class String():
        ...

    class Aggregation:
        ...

    def concat(self, dataframes: Sequence[DataFrame]) -> DataFrame:
        ...

    def column_from_sequence(
        self,
        sequence: Sequence[Any],
        *,
        dtype: Any,
        name: str = "",
    ) -> Column:
        ...

    def dataframe_from_columns(self, *columns: Column) -> DataFrame:
        ...

    def column_from_1d_array(
        self, array: Any, *, dtype: Any, name: str = ""
    ) -> Column:
        ...

    def dataframe_from_2d_array(
        self,
        array: Any,
        *,
        names: Sequence[str],
        dtypes: Mapping[str, Any],
    ) -> DataFrame:
        ...

    def is_null(self, value: object, /) -> bool:
        ...

    def is_dtype(self, dtype: Any, kind: str | tuple[str, ...]) -> bool:
        ...
    
    def date(self, year: int, month: int, day: int) -> Scalar:
        ...

class SupportsDataFrameAPI(Protocol):
    def __dataframe_consortium_standard__(
        self, *, api_version: str | None = None
    ) -> DataFrame:
        ...

class SupportsColumnAPI(Protocol):
    def __column_consortium_standard__(
        self, *, api_version: str | None = None
    ) -> Column:
        ...


__all__ = [
    "Aggregation",
    "Column",
    "DataFrame",
    "DType",
    "GroupBy",
    "Namespace",
    "NullType",
    "Scalar",
    "SupportsColumnAPI",
    "SupportsDataFrameAPI",
    "Scalar",
]
