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
from dataframe_api.groupby_object import GroupBy

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

    @staticmethod
    def Int64() -> Int64:
        ...

    @staticmethod
    def Int32() -> Int32:
        ...

    @staticmethod
    def Int16() -> Int16:
        ...

    @staticmethod
    def Int8() -> Int8:
        ...

    @staticmethod
    def UInt64() -> UInt64:
        ...

    @staticmethod
    def UInt32() -> UInt32:
        ...

    @staticmethod
    def UInt16() -> UInt16:
        ...

    @staticmethod
    def UInt8() -> UInt8:
        ...

    @staticmethod
    def Float64() -> Float64:
        ...

    @staticmethod
    def Float32() -> Float32:
        ...

    @staticmethod
    def Bool() -> Bool:
        ...

    @staticmethod
    def Date() -> Date:
        ...

    @staticmethod
    def Datetime(time_unit: Literal['ms', 'us'], time_zone: str | None) -> Datetime:
        ...

    @staticmethod
    def String() -> String:
        ...

    @staticmethod
    def concat(dataframes: Sequence[DataFrame]) -> DataFrame:
        ...

    @staticmethod
    def column_from_sequence(
        sequence: Sequence[Any],
        *,
        dtype: Any,
        name: str = "",
    ) -> Column:
        ...

    @staticmethod
    def dataframe_from_columns(*columns: Column) -> DataFrame:
        ...

    @staticmethod
    def column_from_1d_array(
        array: Any, *, dtype: Any, name: str = ""
    ) -> Column:
        ...

    @staticmethod
    def dataframe_from_2d_array(
        array: Any,
        *,
        names: Sequence[str],
        dtypes: Mapping[str, Any],
    ) -> DataFrame:
        ...

    @staticmethod
    def is_null(value: object, /) -> bool:
        ...

    @staticmethod
    def is_dtype(dtype: Any, kind: str | tuple[str, ...]) -> bool:
        ...

    @staticmethod
    def date(year: int, month: int, day: int) -> Scalar:
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
