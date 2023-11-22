from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from typing_extensions import Self

    from dataframe_api.typing import AnyScalar, DType

__all__ = ["Scalar"]


class Scalar(Protocol):
    """Scalar object.

    Not meant to be instantiated directly, but rather created via
    `:meth:Column.get_value` or one of the column reductions such
    as `:meth:`Column.sum`.

    Note that, just like how `:class:Column`s can hold null values,
    a `Scalar` can also be backed by a null value. Given that `Scalar`s
    aren't instantiated directly, but rather derived from existing
    `Column`s, `Scalar.dtype` is determined by the parent `Column`.
    For example, if `column` is `Column` of dtype `Int64`, then
    `column.get_value(0)` will return a `Scalar` of dtype `Int64`
    (even if it is backed by a null value).
    """

    def __lt__(self, other: AnyScalar) -> Scalar:
        ...

    def __le__(self, other: AnyScalar) -> Scalar:
        ...

    def __eq__(self, other: AnyScalar) -> Scalar:  # type: ignore[override]
        ...

    def __ne__(self, other: AnyScalar) -> Scalar:  # type: ignore[override]
        ...

    def __gt__(self, other: AnyScalar) -> Scalar:
        ...

    def __ge__(self, other: AnyScalar) -> Scalar:
        ...

    def __add__(self, other: AnyScalar) -> Scalar:
        ...

    def __radd__(self, other: AnyScalar) -> Scalar:
        ...

    def __sub__(self, other: AnyScalar) -> Scalar:
        ...

    def __rsub__(self, other: AnyScalar) -> Scalar:
        ...

    def __mul__(self, other: AnyScalar) -> Scalar:
        ...

    def __rmul__(self, other: AnyScalar) -> Scalar:
        ...

    def __mod__(self, other: AnyScalar) -> Scalar:
        ...

    # Signatures of "__rmod__" of "Scalar" and "__mod__" of "str | int | float | Scalar"
    # are unsafely overlapping
    def __rmod__(self, other: AnyScalar) -> Scalar:  # type: ignore[misc]
        ...

    def __pow__(self, other: AnyScalar) -> Scalar:
        ...

    def __rpow__(self, other: AnyScalar) -> Scalar:
        ...

    def __floordiv__(self, other: AnyScalar) -> Scalar:
        ...

    def __rfloordiv__(self, other: AnyScalar) -> Scalar:
        ...

    def __truediv__(self, other: AnyScalar) -> Scalar:
        ...

    def __rtruediv__(self, other: AnyScalar) -> Scalar:
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

    @property
    def dtype(self) -> DType:
        """Return data type of scalar."""
        ...

    def persist(self) -> Self:
        """Hint that computation prior to this point should not be repeated.

        This is intended as a hint, rather than as a directive. Implementations
        which do not separate lazy vs eager execution may ignore this method and
        treat it as a no-op.

        .. note::
            This may trigger computation and so should be used with care.
            See `execution_model` page for more details.
        """
        ...
