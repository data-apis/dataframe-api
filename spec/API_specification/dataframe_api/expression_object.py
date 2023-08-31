from __future__ import annotations

from typing import Any,NoReturn, TYPE_CHECKING, Literal, Generic

from ._types import DType

if TYPE_CHECKING:
    from . import Bool
    from ._types import NullType, Scalar


__all__ = ['Expression']


class Expression:
    """
    Expression object, which maps a DataFrame to a column.

    Not meant to be used directly - instead, use :func:`dataframe_api.col`.

    An expression is a function which maps a DataFrame to a column, and can be
    used within the context of:

    - :meth:`DataFrame.select`
    - :meth:`DataFrame.insert_column`
    - :meth:`DataFrame.update_columns`
    - :meth:`DataFrame.get_rows_by_mask`

    Example:

    .. code-block::python

        df: DataFrame
        namespace = df.__dataframe_namespace__()
        col = namespace.col
        df = df.select(col(['a', 'b']))
    
    resolves to (pandas syntax):

    .. code-block::python

        df: pd.DataFrame
        df = df.loc[:, ['a', 'b']]
    
    Multiple column calls can be chained together. For example:

    .. code-block::python

        df: DataFrame
        namespace = df.__dataframe_namespace__()
        col = namespace.col
        new_column = (
            (col('petal_width') - col('petal_width').mean())
            .rename('petal_width_centered')
        )
        df = df.insert_column(new_column)
    
    resolves to (pandas syntax)

    .. code-block::python

        df: pd.DataFrame
        new_column = (
            (df['petal_width'] - df['petal_width'].mean())
            .rename('petal_width_centered')
        )
        df[new_column.name] = new_column
    """

    def __len__(self) -> Expression:
        """
        Return the number of rows.
        """

    @property
    def name(self) -> str:
        """Return output name of expression."""

    def slice_rows(
        self: Expression, start: int | None, stop: int | None, step: int | None
    ) -> Expression:
        """
        Select a subset of rows corresponding to a slice.

        Parameters
        ----------
        start : int or None
        stop : int or None
        step : int or None

        Returns
        -------
        Expression
        """
        ...

    def get_rows_by_mask(self, mask: Expression) -> Expression:
        """
        Select a subset of rows corresponding to a mask.

        Parameters
        ----------
        mask : Expression

        Returns
        -------
        Expression
        """
        ...

    def get_value(self, row_number: int) -> Expression:
        """
        Select the value at a row number, similar to `ndarray.__getitem__(<int>)`.

        Parameters
        ----------
        row_number : int
            Row number of value to return.
        
        Returns
        -------
        Expression
        """
        ...

    def sort(
        self,
        *,
        ascending: bool = True,
        nulls_position: Literal['first', 'last'] = 'last',
    ) -> Expression:
        """
        Sort expression.

        If you need the indices which would sort the expression,
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
        Expression
        """
        ...

    def sorted_indices(
        self,
        *,
        ascending: bool = True,
        nulls_position: Literal['first', 'last'] = 'last',
    ) -> Expression:
        """
        Return row numbers which would sort expression.

        If you need to sort the expression, use :meth:`sort`.

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
        Expression
        """
        ...

    def __eq__(self, other: Expression | Scalar) -> Expression:  # type: ignore[override]
        """
        Compare for equality.

        Nulls should follow Kleene Logic.

        Parameters
        ----------
        other : Expression or Scalar
            If expression, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Expression
        """

    def __ne__(self: Expression, other: Expression | Scalar) -> Expression:  # type: ignore[override]
        """
        Compare for non-equality.

        Nulls should follow Kleene Logic.

        Parameters
        ----------
        other : Expression or Scalar
            If expression, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Expression
        """

    def __ge__(self: Expression, other: Expression | Scalar) -> Expression:
        """
        Compare for "greater than or equal to" `other`.

        Parameters
        ----------
        other : Expression or Scalar
            If expression, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Expression
        """

    def __gt__(self: Expression, other: Expression | Scalar) -> Expression:
        """
        Compare for "greater than" `other`.

        Parameters
        ----------
        other : Expression or Scalar
            If expression, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Expression
        """

    def __le__(self: Expression, other: Expression | Scalar) -> Expression:
        """
        Compare for "less than or equal to" `other`.

        Parameters
        ----------
        other : Expression or Scalar
            If expression, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Expression
        """

    def __lt__(self: Expression, other: Expression | Scalar) -> Expression:
        """
        Compare for "less than" `other`.

        Parameters
        ----------
        other : Expression or Scalar
            If expression, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Expression
        """

    def __and__(self: Expression, other: Expression | bool) -> Expression:
        """
        Apply logical 'and' to `other` expression (or scalar) and this expression.

        Nulls should follow Kleene Logic.

        Parameters
        ----------
        other : Expression[bool] or bool
            If expression, must have same length.

        Returns
        -------
        Expression

        Raises
        ------
        ValueError
            If `self` or `other` is not boolean.
        """

    def __or__(self: Expression, other: Expression | bool) -> Expression:
        """
        Apply logical 'or' to `other` expression (or scalar) and this expression.

        Nulls should follow Kleene Logic.

        Parameters
        ----------
        other : Expression[bool] or Scalar
            If expression, must have same length.

        Returns
        -------
        Expression[bool]

        Raises
        ------
        ValueError
            If `self` or `other` is not boolean.
        """

    def __add__(self: Expression, other: Expression | Scalar) -> Expression:
        """
        Add `other` expression or scalar to this expression.

        Parameters
        ----------
        other : Expression or Scalar
            If expression, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Expression
        """

    def __sub__(self: Expression, other: Expression | Scalar) -> Expression:
        """
        Subtract `other` expression or scalar from this expression.

        Parameters
        ----------
        other : Expression or Scalar
            If expression, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Expression
        """

    def __mul__(self, other: Expression | Scalar) -> Expression:
        """
        Multiply `other` expression or scalar with this expression.

        Parameters
        ----------
        other : Expression or Scalar
            If expression, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Expression
        """

    def __truediv__(self, other: Expression | Scalar) -> Expression:
        """
        Divide this expression by `other` expression or scalar. True division, returns floats.

        Parameters
        ----------
        other : Expression or Scalar
            If expression, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Expression
        """

    def __floordiv__(self, other: Expression | Scalar) -> Expression:
        """
        Floor-divide `other` expression or scalar to this expression.

        Parameters
        ----------
        other : Expression or Scalar
            If expression, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Expression
        """

    def __pow__(self, other: Expression | Scalar) -> Expression:
        """
        Raise this expression to the power of `other`.

        Integer dtype to the power of non-negative integer dtype is integer dtype.
        Integer dtype to the power of float dtype is float dtype.
        Float dtype to the power of integer dtype or float dtype is float dtype.

        Parameters
        ----------
        other : Expression or Scalar
            If expression, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Expression
        """

    def __mod__(self, other: Expression | Scalar) -> Expression:
        """
        Returns modulus of this expression by `other` (`%` operator).

        Parameters
        ----------
        other : Expression or Scalar
            If expression, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        Expression
        """

    def __divmod__(self, other: Expression | Scalar) -> tuple[Expression, Expression]:
        """
        Return quotient and remainder of integer division. See `divmod` builtin function.

        Parameters
        ----------
        other : Expression or Scalar
            If expression, must have same length.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        tuple[Expression, Expression]
        """

    def __invert__(self: Expression) -> Expression:
        """
        Invert truthiness of (boolean) elements.

        Raises
        ------
        ValueError
            If any of the expression's expressions is not boolean.
        """

    def any(self: Expression, *, skip_nulls: bool = True) -> Expression:
        """
        Reduction returns a bool.

        Raises
        ------
        ValueError
            If expression is not boolean.
        """

    def all(self: Expression, *, skip_nulls: bool = True) -> Expression:
        """
        Reduction returns a bool.

        Raises
        ------
        ValueError
            If expression is not boolean.
        """

    def min(self, *, skip_nulls: bool = True) -> Expression:
        """
        Reduction returns a scalar. Any data type that supports comparisons
        must be supported. The returned value has the same dtype as the expression.
        """

    def max(self, *, skip_nulls: bool = True) -> Expression:
        """
        Reduction returns a scalar. Any data type that supports comparisons
        must be supported. The returned value has the same dtype as the expression.
        """

    def sum(self, *, skip_nulls: bool = True) -> Expression:
        """
        Reduction returns a scalar. Must be supported for numerical and
        datetime data types. The returned value has the same dtype as the
        expression.
        """

    def prod(self, *, skip_nulls: bool = True) -> Expression:
        """
        Reduction returns a scalar. Must be supported for numerical data types.
        The returned value has the same dtype as the expression.
        """

    def median(self, *, skip_nulls: bool = True) -> Expression:
        """
        Reduction returns a scalar. Must be supported for numerical and
        datetime data types. Returns a float for numerical data types, and
        datetime (with the appropriate timedelta format string) for datetime
        dtypes.
        """

    def mean(self, *, skip_nulls: bool = True) -> Expression:
        """
        Reduction returns a scalar. Must be supported for numerical and
        datetime data types. Returns a float for numerical data types, and
        datetime (with the appropriate timedelta format string) for datetime
        dtypes.
        """

    def std(self, *, correction: int | float = 1, skip_nulls: bool = True) -> Expression:
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
            standard choice (i.e., the provided expression contains data
            constituting an entire population). When computing the corrected
            sample standard deviation, setting this parameter to ``1`` is the
            standard choice (i.e., the provided expression contains data sampled
            from a larger population; this is commonly referred to as Bessel's
            correction). Fractional (float) values are allowed. Default: ``1``.
        skip_nulls
            Whether to skip null values.
        """

    def var(self, *, correction: int | float = 1, skip_nulls: bool = True) -> Expression:
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
            See `expression.std` for a more detailed description.
        skip_nulls
            Whether to skip null values.
        """

    def cumulative_max(self: Expression) -> Expression:
        """
        Reduction returns a expression. Any data type that supports comparisons
        must be supported. The returned value has the same dtype as the expression.
        """

    def cumulative_min(self: Expression) -> Expression:
        """
        Reduction returns a expression. Any data type that supports comparisons
        must be supported. The returned value has the same dtype as the expression.
        """

    def cumulative_sum(self: Expression) -> Expression:
        """
        Reduction returns a expression. Must be supported for numerical and
        datetime data types. The returned value has the same dtype as the
        expression.
        """

    def cumulative_prod(self: Expression) -> Expression:
        """
        Reduction returns a expression. Must be supported for numerical and
        datetime data types. The returned value has the same dtype as the
        expression.
        """

    def is_null(self) -> Expression:
        """
        Check for 'missing' or 'null' entries.

        Returns
        -------
        Expression

        See also
        --------
        is_nan

        Notes
        -----
        Does *not* include NaN-like entries.
        May optionally include 'NaT' values (if present in an implementation),
        but note that the Standard makes no guarantees about them.
        """

    def is_nan(self) -> Expression:
        """
        Check for nan entries.

        Returns
        -------
        Expression

        See also
        --------
        is_null

        Notes
        -----
        This only checks for 'NaN'.
        Does *not* include 'missing' or 'null' entries.
        In particular, does not check for `np.timedelta64('NaT')`.
        """

    def is_in(self: Expression, values: Expression) -> Expression:
        """
        Indicate whether the value at each row matches any value in `values`.

        Parameters
        ----------
        values : Expression
            Contains values to compare against. May include ``float('nan')`` and
            ``null``, in which case ``'nan'`` and ``null`` will
            respectively return ``True`` even though ``float('nan') == float('nan')``
            isn't ``True``.
            The dtype of ``values`` must match the current expression's dtype.

        Returns
        -------
        Expression[bool]
        """

    def unique_indices(self, *, skip_nulls: bool = True) -> Expression:
        """
        Return indices corresponding to unique values in expression.

        Returns
        -------
        Expression[int]
            Indices corresponding to unique values.

        Notes
        -----
        There are no ordering guarantees. In particular, if there are multiple
        indices corresponding to the same unique value, there is no guarantee
        about which one will appear in the result.
        If the original expression contains multiple `'NaN'` values, then
        only a single index corresponding to those values will be returned.
        Likewise for null values (if ``skip_nulls=False``).
        To get the unique values, you can do ``col.get_rows(col.unique_indices())``.
        """
        ...

    def fill_nan(self: Expression, value: float | NullType, /) -> Expression:
        """
        Fill floating point ``nan`` values with the given fill value.

        Parameters
        ----------
        value : float or `null`
            Value used to replace any ``nan`` in the expression with. Must be
            of the Python scalar type matching the dtype of the expression (or
            be `null`).

        """
        ...

    def fill_null(self: Expression, value: Scalar, /) -> Expression:
        """
        Fill null values with the given fill value.

        Parameters
        ----------
        value : Scalar
            Value used to replace any ``null`` values in the expression with.
            Must be of the Python scalar type matching the dtype of the expression.

        """
        ...

    def rename(self, name: str) -> Expression:
        """
        Rename expression.

        Parameters
        ----------
        name : str
            New name for expression.
        
        Returns
        -------
        Expression
            New expression - this does not operate in-place.
        """
        ...
