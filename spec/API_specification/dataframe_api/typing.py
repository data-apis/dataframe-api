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


# null is a special object which represents a missing value.
# It is not valid as a type.


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

    class NullType:
        ...

    null: NullType

    class Datetime:
        time_unit: Literal["ms", "us"]
        time_zone: str | None

        def __init__(  # noqa: ANN204
            self,
            time_unit: Literal["ms", "us"],
            time_zone: str | None = None,
        ):
            ...

    class Duration:
        time_unit: Literal["ms", "us"]

        def __init__(  # noqa: ANN204
            self,
            time_unit: Literal["ms", "us"],
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
        names: Sequence[str],
    ) -> DataFrame:
        ...

    def is_null(self, value: object, /) -> bool:
        ...

    def is_dtype(self, dtype: DType, kind: str | tuple[str, ...]) -> bool:
        ...

    def date(self, year: int, month: int, day: int) -> Scalar:
        ...

    def any_horizontal(
        self,
        *columns: Column,
        skip_nulls: bool = True,
    ) -> Column:
        ...

    def all_horizontal(
        self,
        *columns: Column,
        skip_nulls: bool = True,
    ) -> Column:
        ...

    def sorted_indices(
        self,
        *columns: Column,
        ascending: Sequence[bool] | bool = True,
        nulls_position: Literal["first", "last"] = "last",
    ) -> Column:
        ...

    def unique_indices(
        self,
        *columns: Column,
        skip_nulls: bool = True,
    ) -> Column:
        ...


DType = Union[
    Namespace.Bool,
    Namespace.Float64,
    Namespace.Float32,
    Namespace.Int64,
    Namespace.Int32,
    Namespace.Int16,
    Namespace.Int8,
    Namespace.UInt64,
    Namespace.UInt32,
    Namespace.UInt16,
    Namespace.UInt8,
    Namespace.String,
    Namespace.Date,
    Namespace.Datetime,
    Namespace.Duration,
]


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


PythonScalar = Union[str, int, float, bool]
AnyScalar = Union[PythonScalar, Scalar]
NullType = Namespace.NullType


__all__ = [
    "Column",
    "DataFrame",
    "DType",
    "GroupBy",
    "Namespace",
    "AnyScalar",
    "Scalar",
    "NullType",
    "SupportsColumnAPI",
    "SupportsDataFrameAPI",
]
