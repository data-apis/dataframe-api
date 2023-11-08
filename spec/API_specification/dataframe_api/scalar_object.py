from __future__ import annotations

from typing import Any, Protocol

__all__ = ["Scalar"]


class Scalar(Protocol):
    """Scalar object

    Not meant to be instantiated directly, but rather created via
    `:meth:Column.get_value` or one of the column reductions such
    as `:meth:`Column.sum`.
    """

    def __lt__(self, other: Any) -> Scalar:
        ...

    def __le__(self, other: Any) -> Scalar:
        ...

    def __eq__(self, other: object) -> Scalar:  # type: ignore[override]
        ...

    def __ne__(self, other: object) -> Scalar:  # type: ignore[override]
        ...

    def __gt__(self, other: Any) -> Scalar:
        ...

    def __ge__(self, other: Any) -> Scalar:
        ...

    def __add__(self, other: Any) -> Scalar:
        ...

    def __radd__(self, other: Any) -> Scalar:
        ...

    def __sub__(self, other: Any) -> Scalar:
        ...

    def __rsub__(self, other: Any) -> Scalar:
        ...

    def __mul__(self, other: Any) -> Scalar:
        ...

    def __rmul__(self, other: Any) -> Scalar:
        ...

    def __mod__(self, other: Any) -> Scalar:
        ...

    def __rmod__(self, other: Any) -> Scalar:
        ...

    def __pow__(self, other: Any) -> Scalar:
        ...

    def __rpow__(self, other: Any) -> Scalar:
        ...

    def __floordiv__(self, other: Any) -> Scalar:
        ...

    def __rfloordiv__(self, other: Any) -> Scalar:
        ...

    def __truediv__(self, other: Any) -> Scalar:
        ...

    def __rtruediv__(self, other: Any) -> Scalar:
        ...

    def __neg__(self) -> Scalar:
        ...

    def __abs__(self) -> Scalar:
        ...

    def __bool__(self) -> bool:
        """Note that this return a Python scalar.

        Depending on the implementation, this may raise or trigger computation.
        """
        ...
