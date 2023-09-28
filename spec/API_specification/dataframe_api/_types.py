"""
Types for type annotations used in the dataframe API standard.
"""
from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    List,
    Literal,
    Mapping,
    Optional,
    Protocol,
    Sequence,
    Tuple,
    Union,
)

if TYPE_CHECKING:
    from .dataframe_object import DataFrame as DataFrameType
    from .column_object import Column as ColumnType

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
    )

    DType = Union[Bool, Float64, Float32, Int64, Int32, Int16, Int8, UInt64, UInt32, UInt16, UInt8]

# Type alias: Mypy needs Any, but for readability we need to make clear this
# is a Python scalar (i.e., an instance of `bool`, `int`, `float`, `str`, etc.)
Scalar = Any
# null is a special object which represents a missing value.
# It is not valid as a type.
NullType = Any


class Namespace(Protocol):
    __dataframe_api_version__: str

    @staticmethod
    def DataFrame() -> DataFrameType:
        ...

    @staticmethod
    def Column() -> ColumnType:
        ...

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
    def Date() -> Bool:
        ...

    @staticmethod
    def Datetime(time_unit: Literal['ms', 'us'], time_zone: str | None) -> Bool:
        ...

    @staticmethod
    def String() -> Bool:
        ...

    @staticmethod
    def concat(dataframes: Sequence[DataFrameType]) -> DataFrameType:
        ...

    @staticmethod
    def column_from_sequence(
        sequence: Sequence[Any],
        *,
        dtype: Any,
        name: str = "",
        api_version: str | None = None,
    ) -> ColumnType:
        ...

    @staticmethod
    def dataframe_from_dict(
        data: Mapping[str, ColumnType], *, api_version: str | None = None
    ) -> DataFrameType:
        ...

    @staticmethod
    def column_from_1d_array(
        array: Any, *, dtype: Any, name: str = "", api_version: str | None = None
    ) -> ColumnType:
        ...

    @staticmethod
    def dataframe_from_2d_array(
        array: Any,
        *,
        names: Sequence[str],
        dtypes: Mapping[str, Any],
        api_version: str | None = None,
    ) -> DataFrameType:
        ...

    @staticmethod
    def is_null(value: object, /) -> bool:
        ...

    @staticmethod
    def is_dtype(dtype: Any, kind: str | tuple[str, ...]) -> bool:
        ...


class SupportsDataFrameAPI(Protocol):
    def __dataframe_consortium_standard__(
        self, *, api_version: str | None = None
    ) -> DataFrameType:
        ...

class SupportsColumnAPI(Protocol):
    def __column_consortium_standard__(
        self, *, api_version: str | None = None
    ) -> ColumnType:
        ...


__all__ = [
    "Any",
    "DataFrame",
    "List",
    "Literal",
    "NestedSequence",
    "Optional",
    "PyCapsule",
    "SupportsBufferProtocol",
    "SupportsDLPack",
    "Tuple",
    "Union",
    "Sequence",
    "array",
    "device",
    "DType",
    "ellipsis",
]
