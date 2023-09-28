"""
Types for type annotations used in the dataframe API standard.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import (
    Any,
    List,
    Literal,
    Optional,
    Sequence,
    Tuple,
    Union,
    TYPE_CHECKING,
)
from enum import Enum

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
    "Enum",
]
