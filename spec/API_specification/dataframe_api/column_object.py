from __future__ import annotations

from typing import Any,NoReturn, Sequence, TYPE_CHECKING, Literal, Generic

from ._types import DType

if TYPE_CHECKING:
    from . import Bool, null
    from ._types import Scalar


__all__ = ['Column']


class Column(Generic[DType]):
    """
    Column object

    Note that this column object is not meant to be instantiated directly by
    users of the library implementing the dataframe API standard. Rather, use
    constructor functions or an already-created dataframe object retrieved via

    """

    def __column_namespace__(
        self, /, *, api_version: str | None = None
    ) -> Any:
        """
        Returns an object that has all the Dataframe Standard API functions on it.

        Parameters
        ----------
        api_version: Optional[str]
            String representing the version of the dataframe API specification
            to be returned, in ``'YYYY.MM'`` form, for example, ``'2023.04'``.
            If it is ``None``, it should return the namespace corresponding to
            latest version of the dataframe API specification.  If the given
            version is invalid or not implemented for the given module, an
            error should be raised. Default: ``None``.

        Returns
        -------
        namespace: Any
            An object representing the dataframe API namespace. It should have
            every top-level function defined in the specification as an
            attribute. It may contain other public names as well, but it is
            recommended to only include those names that are part of the
            specification.

        """
    
    @property
    def column(self) -> Any:
        """
        Return underlying (not-necessarily-Standard-compliant) column.

        If a library only implements the Standard, then this can return `self`.
        """
        ...

    def __len__(self) -> int:
        """
        Return the number of rows.
        """

    def __iter__(self) -> NoReturn:
        """
        Iterate over elements.

        This is intentionally "poisoned" to discourage inefficient code patterns.

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError("'__iter__' is intentionally not implemented.")

    @property
    def dtype(self) -> Any:
        """
        Return data type of column.
        """

    def get_rows(self: Column[DType], indices: Column[Any]) -> Column[DType]:
        """
        Select a subset of rows, similar to `ndarray.take`.

        Parameters
        ----------
        indices : Column[int]
            Positions of rows to select.
        """
        ...

    def get_value(self, row_number: int) -> Scalar:
        """
        Select the value at a row number, similar to `ndarray.__getitem__(<int>)`.

        Parameters
        ----------
        row_number : int
            Row number of value to return.
        
        Returns
        -------
        Scalar
            Depends on the dtype of the Column, and may vary
            across implementations.
        """
        ...

    def sorted_indices(
        self,
        *,
        ascending: bool = True,
        nulls_position: Literal['first', 'last'] = 'last',
    ) -> Column[Any]:
        """
        Return row numbers which would sort column.

        If you need to sort the Column, you can simply do::

            col.get_rows(col.sorted_indices())

        Parameters
        ----------
        ascending : bool
            If `True`, sort in ascending order.
            If `False`, sort in descending order.
        nulls_position : ``{'first', 'last'}``
            Whether null values should be placed at the beginning
            or at the end of the result.
            Note that the position of NaNs is unspecified and may
            vary based on the implementation.

        Returns
        -------
        Column[int]
        """
        ...

    def __eq__(self, other: Column[Any] | Scalar) -> Column[Bool]:  # type: ignore[override]
        """
        Compare for equality.

        Nulls should follow Kleene Logic.

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column
        """

    def __ne__(self: Column[DType], other: Column[DType] | Any) -> Column[Bool]:  # type: ignore[override]
        """
        Compare for non-equality.

        Nulls should follow Kleene Logic.

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column
        """

    def __ge__(self: Column[DType], other: Column[DType] | Any) -> Column[Bool]:
        """
        Compare for "greater than or equal to" `other`.

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column
        """

    def __gt__(self: Column[DType], other: Column[DType] | Any) -> Column[Bool]:
        """
        Compare for "greater than" `other`.

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column
        """

    def __le__(self: Column[DType], other: Column[DType] | Any) -> Column[Bool]:
        """
        Compare for "less than or equal to" `other`.

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column
        """

    def __lt__(self: Column[DType], other: Column[DType] | Any) -> Column[Bool]:
        """
        Compare for "less than" `other`.

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column
        """

    def __and__(self: Column[Bool], other: Column[Bool] | bool) -> Column[Bool]:
        """
        Apply logical 'and' to `other` Column (or scalar) and this Column.

        Nulls should follow Kleene Logic.

        Parameters
        ----------
        other : Column[bool] or bool
            If Column, must have same length.

        Returns
        -------
        Column

        Raises
        ------
        ValueError
            If `self` or `other` is not boolean.
        """

    def __or__(self: Column[Bool], other: Column[Bool] | bool) -> Column[Bool]:
        """
        Apply logical 'or' to `other` Column (or scalar) and this column.

        Nulls should follow Kleene Logic.

        Parameters
        ----------
        other : Column[bool] or Scalar
            If Column, must have same length.

        Returns
        -------
        Column[bool]

        Raises
        ------
        ValueError
            If `self` or `other` is not boolean.
        """

    def __add__(self: Column[Any], other: Column[Any] | Scalar) -> Column[Any]:
        """
        Add `other` column or scalar to this column.

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column
        """

    def __sub__(self: Column[Any], other: Column[Any] | Scalar) -> Column[Any]:
        """
        Subtract `other` column or scalar from this column.

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column
        """

    def __mul__(self, other: Column[Any] | Scalar) -> Column[Any]:
        """
        Multiply `other` column or scalar with this column.

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column
        """

    def __truediv__(self, other: Column[Any] | Scalar) -> Column[Any]:
        """
        Divide this column by `other` column or scalar. True division, returns floats.

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column
        """

    def __floordiv__(self, other: Column[Any] | Scalar) -> Column[Any]:
        """
        Floor-divide `other` column or scalar to this column.

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column
        """

    def __pow__(self, other: Column[Any] | Scalar) -> Column[Any]:
        """
        Raise this column to the power of `other`.

        Integer dtype to the power of non-negative integer dtype is integer dtype.
        Integer dtype to the power of float dtype is float dtype.
        Float dtype to the power of integer dtype or float dtype is float dtype.

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column
        """

    def __mod__(self, other: Column[Any] | Scalar) -> Column[Any]:
        """
        Returns modulus of this column by `other` (`%` operator).

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column
        """

    def __divmod__(self, other: Column[Any] | Scalar) -> tuple[Column[Any], Column[Any]]:
        """
        Return quotient and remainder of integer division. See `divmod` builtin function.

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column
        """

    def __invert__(self: Column[Bool]) -> Column[Bool]:
        """
        Invert truthiness of (boolean) elements.

        Raises
        ------
        ValueError
            If any of the Column's columns is not boolean.
        """

    def any(self: Column[Bool], *, skip_nulls: bool = True) -> bool:
        """
        Reduction returns a bool.

        Raises
        ------
        ValueError
            If column is not boolean.
        """

    def all(self: Column[Bool], *, skip_nulls: bool = True) -> bool:
        """
        Reduction returns a bool.

        Raises
        ------
        ValueError
            If column is not boolean.
        """

    def min(self, *, skip_nulls: bool = True) -> Any:
        """
        Reduction returns a scalar. Any data type that supports comparisons
        must be supported. The returned value has the same dtype as the column.
        """

    def max(self, *, skip_nulls: bool = True) -> Any:
        """
        Reduction returns a scalar. Any data type that supports comparisons
        must be supported. The returned value has the same dtype as the column.
        """

    def sum(self, *, skip_nulls: bool = True) -> Any:
        """
        Reduction returns a scalar. Must be supported for numerical and
        datetime data types. The returned value has the same dtype as the
        column.
        """

    def prod(self, *, skip_nulls: bool = True) -> Any:
        """
        Reduction returns a scalar. Must be supported for numerical data types.
        The returned value has the same dtype as the column.
        """

    def median(self, *, skip_nulls: bool = True) -> Any:
        """
        Reduction returns a scalar. Must be supported for numerical and
        datetime data types. Returns a float for numerical data types, and
        datetime (with the appropriate timedelta format string) for datetime
        dtypes.
        """

    def mean(self, *, skip_nulls: bool = True) -> Any:
        """
        Reduction returns a scalar. Must be supported for numerical and
        datetime data types. Returns a float for numerical data types, and
        datetime (with the appropriate timedelta format string) for datetime
        dtypes.
        """

    def std(self, *, correction: int | float = 1, skip_nulls: bool = True) -> Any:
        """
        Reduction returns a scalar. Must be supported for numerical and
        datetime data types. Returns a float for numerical data types, and
        datetime (with the appropriate timedelta format string) for datetime
        dtypes.

        Parameters
        ----------
        correction
            Degrees of freedom adjustment. Setting this parameter to a value other
            than ``0`` has the effect of adjusting the divisor during the
            calculation of the standard deviation according to ``N-correction``,
            where ``N`` corresponds to the total number of elements over which
            the standard deviation is computed. When computing the standard
            deviation of a population, setting this parameter to ``0`` is the
            standard choice (i.e., the provided column contains data
            constituting an entire population). When computing the corrected
            sample standard deviation, setting this parameter to ``1`` is the
            standard choice (i.e., the provided column contains data sampled
            from a larger population; this is commonly referred to as Bessel's
            correction). Fractional (float) values are allowed. Default: ``1``.
        skip_nulls
            Whether to skip null values.
        """

    def var(self, *, correction: int | float = 1, skip_nulls: bool = True) -> Any:
        """
        Reduction returns a scalar. Must be supported for numerical and
        datetime data types. Returns a float for numerical data types, and
        datetime (with the appropriate timedelta format string) for datetime
        dtypes.

        Parameters
        ----------
        correction
            Correction to apply to the result. For example, ``0`` for sample
            standard deviation and ``1`` for population standard deviation.
            See `Column.std` for a more detailed description.
        skip_nulls
            Whether to skip null values.
        """

    def cumulative_max(self: Column[DType]) -> Column[DType]:
        """
        Reduction returns a Column. Any data type that supports comparisons
        must be supported. The returned value has the same dtype as the column.
        """

    def cumulative_min(self: Column[DType]) -> Column[DType]:
        """
        Reduction returns a Column. Any data type that supports comparisons
        must be supported. The returned value has the same dtype as the column.
        """

    def cumulative_sum(self: Column[DType]) -> Column[DType]:
        """
        Reduction returns a Column. Must be supported for numerical and
        datetime data types. The returned value has the same dtype as the
        column.
        """

    def cumulative_prod(self: Column[DType]) -> Column[DType]:
        """
        Reduction returns a Column. Must be supported for numerical and
        datetime data types. The returned value has the same dtype as the
        column.
        """

    def is_null(self) -> Column[Bool]:
        """
        Check for 'missing' or 'null' entries.

        Returns
        -------
        Column

        See also
        --------
        is_nan

        Notes
        -----
        Does *not* include NaN-like entries.
        May optionally include 'NaT' values (if present in an implementation),
        but note that the Standard makes no guarantees about them.
        """

    def is_nan(self) -> Column[Bool]:
        """
        Check for nan entries.

        Returns
        -------
        Column

        See also
        --------
        is_null

        Notes
        -----
        This only checks for 'NaN'.
        Does *not* include 'missing' or 'null' entries.
        In particular, does not check for `np.timedelta64('NaT')`.
        """

    def is_in(self: Column[DType], values: Column[DType]) -> Column[Bool]:
        """
        Indicate whether the value at each row matches any value in `values`.

        Parameters
        ----------
        values : Column
            Contains values to compare against. May include ``float('nan')`` and
            ``null``, in which case ``'nan'`` and ``null`` will
            respectively return ``True`` even though ``float('nan') == float('nan')``
            isn't ``True``.
            The dtype of ``values`` must match the current column's dtype.

        Returns
        -------
        Column[bool]
        """

    def unique_indices(self, *, skip_nulls: bool = True) -> Column[Any]:
        """
        Return indices corresponding to unique values in Column.

        Returns
        -------
        Column[int]
            Indices corresponding to unique values.

        Notes
        -----
        There are no ordering guarantees. In particular, if there are multiple
        indices corresponding to the same unique value, there is no guarantee
        about which one will appear in the result.
        If the original Column contains multiple `'NaN'` values, then
        only a single index corresponding to those values should be returned.
        Likewise for null values (if ``skip_nulls=False``).
        To get the unique values, you can do ``col.get_rows(col.unique_indices())``.
        """
        ...

    def fill_nan(self: Column[DType], value: float | 'null', /) -> Column[DType]:
        """
        Fill floating point ``nan`` values with the given fill value.

        Parameters
        ----------
        value : float or `null`
            Value used to replace any ``nan`` in the column with. Must be
            of the Python scalar type matching the dtype of the column (or
            be `null`).

        """
        ...

    def fill_null(self: Column[DType], value: Scalar, /) -> Column[DType]:
        """
        Fill null values with the given fill value.

        Parameters
        ----------
        value : Scalar
            Value used to replace any ``null`` values in the column with.
            Must be of the Python scalar type matching the dtype of the column.

        """
        ...
