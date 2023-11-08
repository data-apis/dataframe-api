from __future__ import annotations

from typing import Literal


class Int64:
    """Integer type with 64 bits of precision."""


class Int32:
    """Integer type with 32 bits of precision."""


class Int16:
    """Integer type with 16 bits of precision."""


class Int8:
    """Integer type with 8 bits of precision."""


class UInt64:
    """Unsigned integer type with 64 bits of precision."""


class UInt32:
    """Unsigned integer type with 32 bits of precision."""


class UInt16:
    """Unsigned integer type with 16 bits of precision."""


class UInt8:
    """Unsigned integer type with 8 bits of precision."""


class Float64:
    """Floating point type with 64 bits of precision."""


class Float32:
    """Floating point type with 32 bits of precision."""


class Bool:
    """Boolean type with 8 bits of precision."""


class Date:
    """Date type.

    There is no guarantee about the range of dates available.
    """


class Datetime:
    """Datetime type.

    Attributes
    ----------
    time_unit : Literal['ms', 'us']
        Precision of the datetime type. There is no guarantee that the full
        range of dates available for the specified precision is supported.
    time_zone : str | None
        Time zone of the datetime type. Only IANA time zones are supported.
        `None` indicates time-zone-naive data.
    """

    def __init__(self, *, time_unit: Literal["ms", "us"], time_zone: str | None):  # noqa: ANN204
        ...

    time_unit: Literal["ms", "us"]
    time_zone: str | None  # Only IANA time zones are supported


class Duration:
    """Duration type."""

    time_unit: Literal["ms", "us"]


class String:
    """String type."""
