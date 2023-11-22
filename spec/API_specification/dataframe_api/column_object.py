from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, NoReturn, Protocol

if TYPE_CHECKING:
    from typing_extensions import Self

    from .typing import (
        AnyScalar,
        DataFrame,
        DType,
        Namespace,
        NullType,
        Scalar,
    )


__all__ = ["Column"]


class Column(Protocol):
    """Column object.

    Note that this column object is not meant to be instantiated directly by
    users of the library implementing the dataframe API standard. Rather, use
    constructor functions or an already-created dataframe object retrieved via
    :meth:`DataFrame.col`.

    The parent dataframe (which can be retrieved via the :meth:`parent_dataframe`
    property) plays a key role here:

    - If two columns were retrieved from the same dataframe,
      then they can be combined and compared at will.
    - If two columns were retrieved from different dataframes,
      then there is no guarantee about how or whether they can be combined and
      compared, this may vary across implementations.
    - If two columns are both "free-standing" (i.e. not retrieved from a dataframe
      but constructed directly from a 1D array or sequence), then they can be
      combined and compared with each other. Note, however, that there's no guarantee
      about whether they can be compared or combined with columns retrieved from a
      different dataframe, this may vary across implementations.
    """

    @property
    def parent_dataframe(self) -> DataFrame | None:
        """Return parent DataFrame, if present.

        For example, if we have the following

        .. code-block:: python

            df: DataFrame
            column = df.col('a')

        then `column.parent_dataframe` should return `df`.

        On the other hand, if we had:

        .. code-block:: python

            column = column_from_1d_array(...)

        then `column.parent_dataframe` should return `None`.
        """

    def __column_namespace__(self) -> Namespace:
        """Return an object that has all the Dataframe Standard API functions on it.

        Returns
        -------
        namespace: Any
            An object representing the dataframe API namespace. It should have
            every top-level function defined in the specification as an
            attribute. It may contain other public names as well, but it is
            recommended to only include those names that are part of the
            specification.
        """
        ...

    @property
    def column(self) -> Any:
        """Return underlying (not-necessarily-Standard-compliant) column.

        If a library only implements the Standard, then this can return `self`.
        """
        ...

    @property
    def name(self) -> str:
        """Return name of column."""
        ...

    def __len__(self) -> int:
        """Return the number of rows."""
        ...

    def __iter__(self) -> NoReturn:
        """Iterate over elements.

        This is intentionally "poisoned" to discourage inefficient code patterns.

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError("'__iter__' is intentionally not implemented.")

    @property
    def dtype(self) -> DType:
        """Return data type of column."""
        ...

    def get_rows(self, indices: Self) -> Self:
        """Select a subset of rows, similar to `ndarray.take`.

        Parameters
        ----------
        indices
            Positions of rows to select.
        """
        ...

    def slice_rows(
        self,
        start: int | None,
        stop: int | None,
        step: int | None,
    ) -> Self:
        """Select a subset of rows corresponding to a slice.

        Parameters
        ----------
        start : int or None
        stop : int or None
        step : int or None

        Returns
        -------
        Column
        """
        ...

    def filter(self, mask: Self) -> Self:
        """Select a subset of rows corresponding to a mask.

        Parameters
        ----------
        mask : Self

        Returns
        -------
        Column

        Notes
        -----
        Some participants preferred a weaker type Arraylike[bool] for mask,
        where 'Arraylike' denotes an object adhering to the Array API standard.
        """
        ...

    def get_value(self, row_number: int) -> Scalar:
        """Select the value at a row number, similar to `ndarray.__getitem__(<int>)`.

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

    def sort(
        self,
        *,
        ascending: bool = True,
        nulls_position: Literal["first", "last"] = "last",
    ) -> Self:
        """Sort column.

        If you need the indices which would sort the column,
        use `sorted_indices`.

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
        Column
        """
        ...

    def sorted_indices(
        self,
        *,
        ascending: bool = True,
        nulls_position: Literal["first", "last"] = "last",
    ) -> Self:
        """Return row numbers which would sort column.

        If you need to sort the Column, use :meth:`sort`.

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
        Column
        """
        ...

    def __eq__(self, other: Self | AnyScalar) -> Self:  # type: ignore[override]
        """Compare for equality.

        Nulls should follow Kleene Logic.

        Parameters
        ----------
        other : Self or Scalar
            If Column, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column

        Notes
        -----
        `other`'s parent DataFrame must be the same as `self`'s - else,
        the operation is unsupported and may vary across implementations.
        """
        ...

    def __ne__(self, other: Self | AnyScalar) -> Self:  # type: ignore[override]
        """Compare for non-equality.

        Nulls should follow Kleene Logic.

        Parameters
        ----------
        other : Self or Scalar
            If Column, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column

        Notes
        -----
        `other`'s parent DataFrame must be the same as `self`'s - else,
        the operation is unsupported and may vary across implementations.
        """
        ...

    def __ge__(self, other: Self | AnyScalar) -> Self:
        """Compare for "greater than or equal to" `other`.

        Parameters
        ----------
        other : Self or Scalar
            If Column, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column

        Notes
        -----
        `other`'s parent DataFrame must be the same as `self`'s - else,
        the operation is unsupported and may vary across implementations.
        """
        ...

    def __gt__(self, other: Self | AnyScalar) -> Self:
        """Compare for "greater than" `other`.

        Parameters
        ----------
        other : Self or Scalar
            If Column, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column

        Notes
        -----
        `other`'s parent DataFrame must be the same as `self`'s - else,
        the operation is unsupported and may vary across implementations.
        """
        ...

    def __le__(self, other: Self | AnyScalar) -> Self:
        """Compare for "less than or equal to" `other`.

        Parameters
        ----------
        other : Self or Scalar
            If Column, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column

        Notes
        -----
        `other`'s parent DataFrame must be the same as `self`'s - else,
        the operation is unsupported and may vary across implementations.
        """
        ...

    def __lt__(self, other: Self | AnyScalar) -> Self:
        """Compare for "less than" `other`.

        Parameters
        ----------
        other : Self or Scalar
            If Column, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column

        Notes
        -----
        `other`'s parent DataFrame must be the same as `self`'s - else,
        the operation is unsupported and may vary across implementations.
        """
        ...

    def __and__(self, other: Self | bool | Scalar) -> Self:
        """Apply logical 'and' to `other` Column (or scalar) and this Column.

        Nulls should follow Kleene Logic.

        Parameters
        ----------
        other : Self or bool
            If Column, must have same length.

        Returns
        -------
        Column

        Notes
        -----
        `other`'s parent DataFrame must be the same as `self`'s - else,
        the operation is unsupported and may vary across implementations.

        Raises
        ------
        ValueError
            If `self` or `other` is not boolean.
        """
        ...

    def __or__(self, other: Self | bool | Scalar) -> Self:
        """Apply logical 'or' to `other` Column (or scalar) and this column.

        Nulls should follow Kleene Logic.

        Parameters
        ----------
        other : Self or Scalar
            If Column, must have same length.

        Returns
        -------
        Column

        Notes
        -----
        `other`'s parent DataFrame must be the same as `self`'s - else,
        the operation is unsupported and may vary across implementations.

        Raises
        ------
        ValueError
            If `self` or `other` is not boolean.
        """
        ...

    def __add__(self, other: Self | AnyScalar) -> Self:
        """Add `other` column or scalar to this column.

        Parameters
        ----------
        other : Self or Scalar
            If Column, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Notes
        -----
        `other`'s parent DataFrame must be the same as `self`'s - else,
        the operation is unsupported and may vary across implementations.

        Returns
        -------
        Column
        """
        ...

    def __sub__(self, other: Self | AnyScalar) -> Self:
        """Subtract `other` column or scalar from this column.

        Parameters
        ----------
        other : Self or Scalar
            If Column, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column

        Notes
        -----
        `other`'s parent DataFrame must be the same as `self`'s - else,
        the operation is unsupported and may vary across implementations.
        """
        ...

    def __mul__(self, other: Self | AnyScalar) -> Self:
        """Multiply `other` column or scalar with this column.

        Parameters
        ----------
        other : Self or Scalar
            If Column, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column

        Notes
        -----
        `other`'s parent DataFrame must be the same as `self`'s - else,
        the operation is unsupported and may vary across implementations.
        """
        ...

    def __truediv__(self, other: Self | AnyScalar) -> Self:
        """Divide this column by `other` column or scalar. True division, returns floats.

        Parameters
        ----------
        other : Self or Scalar
            If Column, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column

        Notes
        -----
        `other`'s parent DataFrame must be the same as `self`'s - else,
        the operation is unsupported and may vary across implementations.
        """
        ...

    def __floordiv__(self, other: Self | AnyScalar) -> Self:
        """Floor-divide `other` column or scalar to this column.

        Parameters
        ----------
        other : Self or Scalar
            If Column, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column

        Notes
        -----
        `other`'s parent DataFrame must be the same as `self`'s - else,
        the operation is unsupported and may vary across implementations.
        """
        ...

    def __pow__(self, other: Self | AnyScalar) -> Self:
        """Raise this column to the power of `other`.

        Integer dtype to the power of non-negative integer dtype is integer dtype.
        Integer dtype to the power of float dtype is float dtype.
        Float dtype to the power of integer dtype or float dtype is float dtype.

        Parameters
        ----------
        other : Self or Scalar
            If Column, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column

        Notes
        -----
        `other`'s parent DataFrame must be the same as `self`'s - else,
        the operation is unsupported and may vary across implementations.
        """
        ...

    def __mod__(self, other: Self | AnyScalar) -> Self:
        """Return modulus of this column by `other` (`%` operator).

        Parameters
        ----------
        other : Self or Scalar
            If Column, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column

        Notes
        -----
        `other`'s parent DataFrame must be the same as `self`'s - else,
        the operation is unsupported and may vary across implementations.
        """
        ...

    def __divmod__(self, other: Self | AnyScalar) -> tuple[Column, Column]:
        """Return quotient and remainder of integer division. See `divmod` builtin.

        Parameters
        ----------
        other : Self or Scalar
            If Column, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column

        Notes
        -----
        `other`'s parent DataFrame must be the same as `self`'s - else,
        the operation is unsupported and may vary across implementations.
        """
        ...

    def __radd__(self, other: Self | AnyScalar) -> Self:
        ...

    def __rsub__(self, other: Self | AnyScalar) -> Self:
        ...

    def __rmul__(self, other: Self | AnyScalar) -> Self:
        ...

    def __rtruediv__(self, other: Self | AnyScalar) -> Self:
        ...

    def __rand__(self, other: Self | bool) -> Self:
        ...

    def __ror__(self, other: Self | bool) -> Self:
        ...

    def __rfloordiv__(self, other: Self | AnyScalar) -> Self:
        ...

    def __rpow__(self, other: Self | AnyScalar) -> Self:
        ...

    def __rmod__(self, other: Self | AnyScalar) -> Self:
        ...

    def __invert__(self) -> Self:
        """Invert truthiness of (boolean) elements.

        Raises
        ------
        ValueError
            If any of the Column's columns is not boolean.
        """
        ...

    def any(self, *, skip_nulls: bool | Scalar = True) -> Scalar:
        """Reduction returns a bool.

        Raises
        ------
        ValueError
            If column is not boolean.
        """
        ...

    def all(self, *, skip_nulls: bool | Scalar = True) -> Scalar:
        """Reduction returns a bool.

        Raises
        ------
        ValueError
            If column is not boolean.
        """
        ...

    def min(self, *, skip_nulls: bool | Scalar = True) -> Scalar:
        """Reduction returns a scalar.

        Any data type that supports comparisons
        must be supported. The returned value has the same dtype as the column.
        """
        ...

    def max(self, *, skip_nulls: bool | Scalar = True) -> Scalar:
        """Reduction returns a scalar.

        Any data type that supports comparisons
        must be supported. The returned value has the same dtype as the column.
        """
        ...

    def sum(self, *, skip_nulls: bool | Scalar = True) -> Scalar:
        """Reduction returns a scalar.

        Must be supported for numerical and
        datetime data types. The returned value has the same dtype as the
        column.
        """
        ...

    def prod(self, *, skip_nulls: bool | Scalar = True) -> Scalar:
        """Reduction returns a scalar.

        Must be supported for numerical data types.
        The returned value has the same dtype as the column.
        """
        ...

    def median(self, *, skip_nulls: bool | Scalar = True) -> Scalar:
        """Reduction returns a scalar.

        Must be supported for numerical and
        datetime data types. Returns a float for numerical data types, and
        datetime (with the appropriate timedelta format string) for datetime
        dtypes.
        """
        ...

    def mean(self, *, skip_nulls: bool | Scalar = True) -> Scalar:
        """Reduction returns a scalar.

        Must be supported for numerical and
        datetime data types. Returns a float for numerical data types, and
        datetime (with the appropriate timedelta format string) for datetime
        dtypes.
        """
        ...

    def std(
        self,
        *,
        correction: float = 1,
        skip_nulls: bool | Scalar = True,
    ) -> Scalar:
        """Reduction returns a scalar.

        Must be supported for numerical and
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
        ...

    def var(
        self,
        *,
        correction: float | Scalar = 1,
        skip_nulls: bool | Scalar = True,
    ) -> Scalar:
        """Reduction returns a scalar.

        Must be supported for numerical and
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
        ...

    def cumulative_max(self) -> Self:
        """Reduction returns a Column.

        Any data type that supports comparisons
        must be supported. The returned value has the same dtype as the column.
        """
        ...

    def cumulative_min(self) -> Self:
        """Reduction returns a Column.

        Any data type that supports comparisons
        must be supported. The returned value has the same dtype as the column.
        """
        ...

    def cumulative_sum(self) -> Self:
        """Reduction returns a Column.

        Must be supported for numerical and
        datetime data types. The returned value has the same dtype as the
        column.
        """
        ...

    def cumulative_prod(self) -> Self:
        """Reduction returns a Column.

        Must be supported for numerical and
        datetime data types. The returned value has the same dtype as the
        column.
        """
        ...

    def is_null(self) -> Self:
        """Check for 'missing' or 'null' entries.

        Returns
        -------
        Column

        See Also
        --------
        is_nan

        Notes
        -----
        Does *not* include NaN-like entries.
        May optionally include 'NaT' values (if present in an implementation),
        but note that the Standard makes no guarantees about them.
        """
        ...

    def is_nan(self) -> Self:
        """Check for nan entries.

        Returns
        -------
        Column

        See Also
        --------
        is_null

        Notes
        -----
        This only checks for 'NaN'.
        Does *not* include 'missing' or 'null' entries.
        In particular, does not check for `np.timedelta64('NaT')`.
        """
        ...

    def is_in(self, values: Self) -> Self:
        """Indicate whether the value at each row matches any value in `values`.

        Parameters
        ----------
        values : Self
            Contains values to compare against. May include ``float('nan')`` and
            ``null``, in which case ``'nan'`` and ``null`` will
            respectively return ``True`` even though ``float('nan') == float('nan')``
            isn't ``True``.
            The dtype of ``values`` must match the current column's dtype.

        Returns
        -------
        Column
        """
        ...

    def unique_indices(self, *, skip_nulls: bool | Scalar = True) -> Self:
        """Return indices corresponding to unique values in Column.

        Returns
        -------
        Column
            Indices corresponding to unique values.

        Notes
        -----
        There are no ordering guarantees. In particular, if there are multiple
        indices corresponding to the same unique value, there is no guarantee
        about which one will appear in the result.
        If the original Column contains multiple `'NaN'` values, then
        only a single index corresponding to those values will be returned.
        Likewise for null values (if ``skip_nulls=False``).
        To get the unique values, you can do ``col.get_rows(col.unique_indices())``.
        """
        ...

    def fill_nan(self, value: float | NullType | Scalar, /) -> Self:
        """Fill floating point ``nan`` values with the given fill value.

        Parameters
        ----------
        value : float or `null`
            Value used to replace any ``nan`` in the column with. Must be
            of the Python scalar type matching the dtype of the column (or
            be `null`).

        """
        ...

    def fill_null(self, value: AnyScalar, /) -> Self:
        """Fill null values with the given fill value.

        Parameters
        ----------
        value : Scalar
            Value used to replace any ``null`` values in the column with.
            Must be of the Python scalar type matching the dtype of the column.

        """
        ...

    def to_array(self) -> Any:
        """Convert to array-API-compliant object.

        The resulting array will have the corresponding dtype from the
        Array API:

        - Bool() -> 'bool'
        - Int8() -> 'int8'
        - Int16() -> 'int16'
        - Int32() -> 'int32'
        - Int64() -> 'int64'
        - UInt8() -> 'uint8'
        - UInt16() -> 'uint16'
        - UInt32() -> 'uint32'
        - UInt64() -> 'uint64'
        - Float32() -> 'float32'
        - Float64() -> 'float64'

        Null values are not supported and must be filled prior to conversion.

        Returns
        -------
        Any
            An array-API-compliant object.

        Notes
        -----
        While numpy arrays are not yet array-API-compliant, implementations
        may choose to return a numpy array (for numpy prior to 2.0), with the
        understanding that consuming libraries would then use the
        ``array-api-compat`` package to convert it to a Standard-compliant array.
        """
        ...

    def rename(self, name: str | Scalar) -> Self:
        """Rename column.

        Parameters
        ----------
        name : str
            New name for column.

        Returns
        -------
        Column
            New column - this does not operate in-place.
        """
        ...

    def shift(self, offset: int | Scalar) -> Self:
        """Shift values by `offset` positions, filling missing values with `null`.

        For example, if the original column contains values `[1, 4, 2]`, then:

        - `.shift(1)` will return `[null, 1, 4]`,
        - `.shift(-1)` will return `[4, 2, null]`,

        Parameters
        ----------
        offset : int
            How many positions to shift by.
        """
        ...

    # --- temporal methods ---

    def year(self) -> Self:
        """Return 'year' component of each element of `Date` and `Datetime` columns.

        For example, return 1981 for 1981-01-02T12:34:56.123456.

        Return column should be of (signed) integer dtype.
        """
        ...

    def month(self) -> Self:
        """Return 'month' component of each element of `Date` and `Datetime` columns.

        For example, return 1 for 1981-01-02T12:34:56.123456.

        Return column should be of integer dtype (signed or unsigned).
        """
        ...

    def day(self) -> Self:
        """Return 'day' component of each element of `Date` and `Datetime` columns.

        For example, return 2 for 1981-01-02T12:34:56.123456.

        Return column should be of integer dtype (signed or unsigned).
        """
        ...

    def hour(self) -> Self:
        """Return 'hour' component of each element of `Date` and `Datetime` columns.

        For example, return 12 for 1981-01-02T12:34:56.123456.

        Return column should be of integer dtype (signed or unsigned).
        """
        ...

    def minute(self) -> Self:
        """Return 'minute' component of each element of `Date` and `Datetime` columns.

        For example, return 34 for 1981-01-02T12:34:56.123456.

        Return column should be of integer dtype (signed or unsigned).
        """
        ...

    def second(self) -> Self:
        """Return 'second' component of each element.

        For example, return 56 for 1981-01-02T12:34:56.123456.

        Only supported for `Date` and `Datetime` columns.
        Return column should be of integer dtype (signed or unsigned).
        """
        ...

    def microsecond(self) -> Self:
        """Return number of microseconds since last second.

        For example, return 123456 for 1981-01-02T12:34:56.123456.

        Only supported for `Date` and `Datetime` columns.
        Return column should be of integer dtype (signed or unsigned).
        """
        ...

    def iso_weekday(self) -> Self:
        """Return ISO weekday for each element of `Date` and `Datetime` columns.

        Note that Monday=1, ..., Sunday=7.

        Return column should be of integer dtype (signed or unsigned).
        """
        ...

    def unix_timestamp(self, *, time_unit: str | Scalar = "s") -> Self:
        """Return number of seconds / milliseconds / microseconds since the Unix epoch.

        The Unix epoch is 00:00:00 UTC on 1 January 1970.

        Parameters
        ----------
        time_unit
            Time unit to use. Must be one of 's', 'ms', or 'us'.

        Returns
        -------
        Column
            Integer data type. For example, if the date is 1970-01-02T00:00:00.123456,
            and the time_unit is ``'s'``, then the result should be 86400, and not
            86400.123456. Information smaller than the given time unit should be
            discarded.
        """
        ...

    def persist(self) -> Self:
        """Hint that computation prior to this point should not be repeated.

        This is intended as a hint, rather than as a directive. Implementations
        which do not separate lazy vs eager execution may ignore this method and
        treat it as a no-op.

        .. note::
            This method may trigger execution. If necessary, it should be called
            at most once per dataframe, and as late as possible in the pipeline.
        """
        ...
