from __future__ import annotations

from typing import Any,NoReturn, TYPE_CHECKING, Literal, Generic


if TYPE_CHECKING:
    from ._types import NullType, Scalar, Namespace
    from .permissivecolumn_object import PermissiveColumn


__all__ = ['Column']


class Column:
    """
    Column object, which maps a DataFrame to a column derived from it.

    Not meant to be instantiated directly - instead, use one of:
    
    - :func:`dataframe_api.col`
    - :func:`dataframe_api.any_rowwise`
    - :func:`dataframe_api.all_rowwise`
    - :func:`dataframe_api.sorted_indices`
    - :func:`dataframe_api.unique_indices`

    A column is lazy and only takes effect when passed to one of the following:

    - :meth:`DataFrame.select`
    - :meth:`DataFrame.assign`
    - :meth:`DataFrame.filter`
    - :meth:`PermissiveFrame.select`
    - :meth:`PermissiveFrame.assign`
    - :meth:`PermissiveFrame.filter`

    For example:

    .. code-block::python

        df: DataFrame
        col = df.__dataframe_namespace__().col
        df = df.filter(col('a') > col('b')*2)
    
    acts like (pandas syntax):

    .. code-block::python

        df: pd.DataFrame
        col_a = lambda df: df.loc[:, 'a']
        col_b = lambda df: df.loc[:, 'b']
        col_b_doubled = lambda df: col_b(df) * 2
        mask = lambda df: col_a(df) > col_b_doubled(df)
        df = df.loc[mask(df)]
    
    Notes
    -----
    Binary operations between columns require that they resolve to columns of the
    same length (unless one of them is of length-1, in which case it is broadcast to
    the same length as the other one).
    For example, the output column resulting from

    .. code-block::python

        col('a') - col('a').mean()
    
    will be the same length as column `'a'` (where its mean will have been subtracted from
    each element).
    """

    def __column_namespace__(self) -> Namespace:
        """
        Returns an object that has all the Dataframe Standard API functions on it.

        Returns
        -------
        namespace: Namespace
            An object representing the dataframe API namespace. It should have
            every top-level function defined in the specification as an
            attribute. It may contain other public names as well, but it is
            recommended to only include those names that are part of the
            specification.

        """

    def root_names(self) -> list[str]:
        """
        Subset of column names to consider from original dataframe when building new column.

        Returns
        -------
        list[str]
            Column names

        Examples
        --------
        >>> col('a').root_names()
        ['a']
        >>> ((col('a') + 1) > col('b')).root_names()
        ['a', 'b']
        >>> any_rowwise('a', 'b').root_names()
        ['a', 'b']
        """

    def output_name(self) -> str:
        """
        Name of resulting column.
        
        Examples
        --------
        >>> col('a').output_name()
        'a'
        >>> col('a').rename('b').output_name()
        'b'
        >>> df.select(col('a').rename('b')).column_names
        ['b']
        """

    def len(self) -> Column:
        """
        Return the number of rows.
        """

    def get_rows(self, indices: Column | PermissiveColumn) -> Column:
        """
        Select a subset of rows, similar to `ndarray.take`.

        Parameters
        ----------
        indices : Column
            Positions of rows to select.
        """
        ...

    def slice_rows(
        self, start: int | None, stop: int | None, step: int | None
    ) -> Column:
        """
        Select a subset of rows corresponding to a slice.

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

    def filter(self, mask: Column | PermissiveColumn) -> Column:
        """
        Select a subset of rows corresponding to a mask.

        Parameters
        ----------
        mask : Column

        Returns
        -------
        Column
        """
        ...

    def get_value(self, row_number: int) -> Column:
        """
        Select the value at a row number, similar to `ndarray.__getitem__(<int>)`.

        Parameters
        ----------
        row_number : int
            Row number of value to return.
        
        Returns
        -------
        Column
        """
        ...

    def sort(
        self,
        *,
        ascending: bool = True,
        nulls_position: Literal['first', 'last'] = 'last',
    ) -> Column:
        """
        Sort column.

        If you need the indices which would sort the column,
        use :func:`sorted_indices`.

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
        nulls_position: Literal['first', 'last'] = 'last',
    ) -> Column:
        """
        Return row numbers which would sort column.

        If you need to sort the column, use :meth:`sort`.

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

    def __eq__(self, other: Column | Scalar) -> Column:  # type: ignore[override]
        """
        Compare for equality.

        Nulls should follow Kleene Logic.

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length or have length 1.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column
        """

    def __ne__(self, other: Column | Scalar) -> Column:  # type: ignore[override]
        """
        Compare for non-equality.

        Nulls should follow Kleene Logic.

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length or have length 1.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column
        """

    def __ge__(self, other: Column | Scalar) -> Column:
        """
        Compare for "greater than or equal to" `other`.

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length or have length 1.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column
        """

    def __gt__(self, other: Column | Scalar) -> Column:
        """
        Compare for "greater than" `other`.

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length or have length 1.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column
        """

    def __le__(self, other: Column | Scalar) -> Column:
        """
        Compare for "less than or equal to" `other`.

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length or have length 1.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column
        """

    def __lt__(self, other: Column | Scalar) -> Column:
        """
        Compare for "less than" `other`.

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length or have length 1.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column
        """

    def __and__(self, other: Column | bool) -> Column:
        """
        Apply logical 'and' to `other` column (or scalar) and this column.

        Nulls should follow Kleene Logic.

        Parameters
        ----------
        other : Column or bool
            If Column, must have same length or have length 1.

        Returns
        -------
        Column

        Raises
        ------
        ValueError
            If `self` or `other` is not boolean.
        """

    def __or__(self, other: Column | bool) -> Column:
        """
        Apply logical 'or' to `other` column (or scalar) and this column.

        Nulls should follow Kleene Logic.

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length or have length 1.

        Returns
        -------
        Column

        Raises
        ------
        ValueError
            If `self` or `other` is not boolean.
        """

    def __add__(self, other: Column | Scalar) -> Column:
        """
        Add `other` column or scalar to this column.

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length or have length 1.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column
        """

    def __sub__(self, other: Column | Scalar) -> Column:
        """
        Subtract `other` column or scalar from this column.

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length or have length 1.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column
        """

    def __mul__(self, other: Column | Scalar) -> Column:
        """
        Multiply `other` column or scalar with this column.

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length or have length 1.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column
        """

    def __truediv__(self, other: Column | Scalar) -> Column:
        """
        Divide this column by `other` column or scalar. True division, returns floats.

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length or have length 1.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column
        """

    def __floordiv__(self, other: Column | Scalar) -> Column:
        """
        Floor-divide `other` column or scalar to this column.

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length or have length 1.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column
        """

    def __pow__(self, other: Column | Scalar) -> Column:
        """
        Raise this column to the power of `other`.

        Integer dtype to the power of non-negative integer dtype is integer dtype.
        Integer dtype to the power of float dtype is float dtype.
        Float dtype to the power of integer dtype or float dtype is float dtype.

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length or have length 1.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column
        """

    def __mod__(self, other: Column | Scalar) -> Column:
        """
        Returns modulus of this column by `other` (`%` operator).

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length or have length 1.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Column
        """

    def __divmod__(self, other: Column | Scalar) -> tuple[Column, Column]:
        """
        Return quotient and remainder of integer division. See `divmod` builtin function.

        Parameters
        ----------
        other : Column or Scalar
            If Column, must have same length or have length 1.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        tuple[Column, Column]
        """

    def __invert__(self) -> Column:
        """
        Invert truthiness of (boolean) elements.

        Raises
        ------
        ValueError
            If the column is not boolean.
        """

    def any(self, *, skip_nulls: bool = True) -> Column:
        """
        Reduction returns a bool.

        Raises
        ------
        ValueError
            If Column is not boolean.
        """

    def all(self, *, skip_nulls: bool = True) -> Column:
        """
        Reduction returns a bool.

        Raises
        ------
        ValueError
            If Column is not boolean.
        """

    def min(self, *, skip_nulls: bool = True) -> Column:
        """
        Reduction returns a scalar. Any data type that supports comparisons
        must be supported. The returned value has the same dtype as the column.
        """

    def max(self, *, skip_nulls: bool = True) -> Column:
        """
        Reduction returns a scalar. Any data type that supports comparisons
        must be supported. The returned value has the same dtype as the column.
        """

    def sum(self, *, skip_nulls: bool = True) -> Column:
        """
        Reduction returns a scalar. Must be supported for numerical and
        datetime data types. The returned value has the same dtype as the
        column.
        """

    def prod(self, *, skip_nulls: bool = True) -> Column:
        """
        Reduction returns a scalar. Must be supported for numerical data types.
        The returned value has the same dtype as the column.
        """

    def median(self, *, skip_nulls: bool = True) -> Column:
        """
        Reduction returns a scalar. Must be supported for numerical and
        datetime data types. Returns a float for numerical data types, and
        datetime (with the appropriate timedelta format string) for datetime
        dtypes.
        """

    def mean(self, *, skip_nulls: bool = True) -> Column:
        """
        Reduction returns a scalar. Must be supported for numerical and
        datetime data types. Returns a float for numerical data types, and
        datetime (with the appropriate timedelta format string) for datetime
        dtypes.
        """

    def std(self, *, correction: int | float = 1, skip_nulls: bool = True) -> Column:
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

    def var(self, *, correction: int | float = 1, skip_nulls: bool = True) -> Column:
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
            See :meth`Column.std` for a more detailed description.
        skip_nulls
            Whether to skip null values.
        """

    def cumulative_max(self) -> Column:
        """
        Reduction returns a column. Any data type that supports comparisons
        must be supported. The returned value has the same dtype as the column.
        """

    def cumulative_min(self) -> Column:
        """
        Reduction returns a column. Any data type that supports comparisons
        must be supported. The returned value has the same dtype as the column.
        """

    def cumulative_sum(self) -> Column:
        """
        Reduction returns a column. Must be supported for numerical and
        datetime data types. The returned value has the same dtype as the
        column.
        """

    def cumulative_prod(self) -> Column:
        """
        Reduction returns a column. Must be supported for numerical and
        datetime data types. The returned value has the same dtype as the
        column.
        """

    def is_null(self) -> Column:
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

    def is_nan(self) -> Column:
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

    def is_in(self, values: Column | PermissiveColumn) -> Column:
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
        Column
        """

    def unique_indices(self, *, skip_nulls: bool = True) -> Column:
        """
        Return indices corresponding to unique values in column.

        Returns
        -------
        Column
            Indices corresponding to unique values.

        Notes
        -----
        There are no ordering guarantees. In particular, if there are multiple
        indices corresponding to the same unique value, there is no guarantee
        about which one will appear in the result.
        If the original column contains multiple `'NaN'` values, then
        only a single index corresponding to those values will be returned.
        Likewise for null values (if ``skip_nulls=False``).
        To get the unique values, you can do ``col.get_rows(col.unique_indices())``.
        """
        ...

    def fill_nan(self, value: float | NullType, /) -> Column:
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

    def fill_null(self, value: Scalar, /) -> Column:
        """
        Fill null values with the given fill value.

        Parameters
        ----------
        value : Scalar
            Value used to replace any ``null`` values in the column with.
            Must be of the Python scalar type matching the dtype of the column.

        """
        ...

    def rename(self, name: str) -> Column:
        """
        Rename column.

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
