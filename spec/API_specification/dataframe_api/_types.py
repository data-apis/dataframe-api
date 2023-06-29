"""
Types for type annotations used in the dataframe API standard.

The type variables should be replaced with the actual types for a given
library, e.g., for Pandas TypeVar('DataFrame') would be replaced with pd.DataFrame.
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
    TypeVar,
    Union,
    Protocol,
    TYPE_CHECKING,
)
from enum import Enum

array = TypeVar("array")
Scalar = TypeVar("Scalar")
device = TypeVar("device")
DType = TypeVar("DType")
SupportsDLPack = TypeVar("SupportsDLPack")
SupportsBufferProtocol = TypeVar("SupportsBufferProtocol")
PyCapsule = TypeVar("PyCapsule")
# ellipsis cannot actually be imported from anywhere, so include a dummy here
# to keep pyflakes happy. https://github.com/python/typeshed/issues/3556
ellipsis = TypeVar("ellipsis")

_T_co = TypeVar("_T_co", covariant=True)


class NestedSequence(Protocol[_T_co]):
    def __getitem__(self, key: int, /) -> Union[_T_co, NestedSequence[_T_co]]:
        ...

    def __len__(self, /) -> int:
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
    "Enum",
]
