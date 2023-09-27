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
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from .dataframe_object import DataFrame

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

    class DataFrame:
        ...

    class Column:
        ...

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

    @staticmethod
    def concat(dataframes: Sequence[DataFrame]) -> DataFrame:
        ...

    @staticmethod
    def column_from_sequence(
        sequence: Sequence[Any],
        *,
        dtype: Any,
        name: str = "",
        api_version: str | None = None,
    ) -> Column:
        ...

    @staticmethod
    def dataframe_from_dict(
        data: Mapping[str, Column], *, api_version: str | None = None
    ) -> DataFrame:
        ...

    @staticmethod
    def column_from_1d_array(
        array: Any, *, dtype: Any, name: str = "", api_version: str | None = None
    ) -> Column:
        ...

    @staticmethod
    def dataframe_from_2d_array(
        array: Any,
        *,
        names: Sequence[str],
        dtypes: Mapping[str, Any],
        api_version: str | None = None,
    ) -> DataFrame:
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
    ) -> DataFrame:
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
