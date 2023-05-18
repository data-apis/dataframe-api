from __future__ import annotations

from typing import NoReturn, Sequence, TYPE_CHECKING

if TYPE_CHECKING:
    from ._types import Scalar, DType


__all__ = ['Column']


class Column:
    """
    Column object

    Note that this column object is not meant to be instantiated directly by
    users of the library implementing the dataframe API standard. Rather, use
    constructor functions or an already-created dataframe object retrieved via

    """
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
    def dtype(self) -> DType:
        """
        Return data type of column.
        """

    def get_rows(self, indices: Column[int]) -> Column:
        """
        Select a subset of rows, similar to `ndarray.take`.

        Parameters
        ----------
        indices : Column[int]
            Positions of rows to select.
        """
        ...

    def get_value(self, row_number: int) -> DType:
        """
        Select the value at a row number, similar to `ndarray.__getitem__(<int>)`.

        Parameters
        ----------
        row_number : int
            Row number of value to return.
        
        Returns
        -------
        dtype
            Depends on the dtype of the Column, and may vary
            across implementations.
        """
        ...

    def __eq__(self, other: Column | Scalar) -> Column:
        """
        Compare for equality.

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

    def __ne__(self, other: Column | Scalar) -> Column:
        """
        Compare for non-equality.

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

    def __ge__(self, other: Column | Scalar) -> Column:
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

    def __gt__(self, other: Column | Scalar) -> Column:
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

    def __le__(self, other: Column | Scalar) -> Column:
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

    def __lt__(self, other: Column | Scalar) -> Column:
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

    def __and__(self, other: Column[bool] | bool) -> Column:
        """
        Apply logical 'and' to `other` Column (or scalar) and this Column.

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

    def __or__(self, other: Column[bool] | bool) -> Column:
        """
        Apply logical 'or' to `other` Column (or scalar) and this column.

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

    def __add__(self, other: Column | Scalar) -> Column:
        """
        Add `other` column or scalar from this column.

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

    def __sub__(self, other: Column | Scalar) -> Column:
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

    def __mul__(self, other: Column | Scalar) -> Column:
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

    def __truediv__(self, other: Column | Scalar) -> Column:
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

    def __floordiv__(self, other: Column | Scalar) -> Column:
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

    def __pow__(self, other: Column | Scalar) -> Column:
        """
        Raise this column to the power of `other`.

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

    def __mod__(self, other: Column | Scalar) -> Column:
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

    def __divmod__(self, other: Column | Scalar) -> tuple[Column, Column]:
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

    def __invert__(self) -> Column:
        """
        Invert truthiness of (boolean) elements.

        Raises
        ------
        ValueError
            If any of the Column's columns is not boolean.
        """

    def any(self, *, skip_nulls: bool = True) -> bool:
        """
        Reduction returns a bool.

        Raises
        ------
        ValueError
            If column is not boolean.
        """

    def all(self, *, skip_nulls: bool = True) -> bool:
        """
        Reduction returns a bool.

        Raises
        ------
        ValueError
            If column is not boolean.
        """

    def min(self, *, skip_nulls: bool = True) -> DType:
        """
        Reduction returns a scalar. Any data type that supports comparisons
        must be supported. The returned value has the same dtype as the column.
        """

    def max(self, *, skip_nulls: bool = True) -> DType:
        """
        Reduction returns a scalar. Any data type that supports comparisons
        must be supported. The returned value has the same dtype as the column.
        """

    def sum(self, *, skip_nulls: bool = True) -> DType:
        """
        Reduction returns a scalar. Must be supported for numerical and
        datetime data types. The returned value has the same dtype as the
        column.
        """

    def prod(self, *, skip_nulls: bool = True) -> DType:
        """
        Reduction returns a scalar. Must be supported for numerical data types.
        The returned value has the same dtype as the column.
        """

    def median(self, *, skip_nulls: bool = True) -> DType:
        """
        Reduction returns a scalar. Must be supported for numerical and
        datetime data types. Returns a float for numerical data types, and
        datetime (with the appropriate timedelta format string) for datetime
        dtypes.
        """

    def mean(self, *, skip_nulls: bool = True) -> DType:
        """
        Reduction returns a scalar. Must be supported for numerical and
        datetime data types. Returns a float for numerical data types, and
        datetime (with the appropriate timedelta format string) for datetime
        dtypes.
        """

    def std(self, *, skip_nulls: bool = True) -> DType:
        """
        Reduction returns a scalar. Must be supported for numerical and
        datetime data types. Returns a float for numerical data types, and
        datetime (with the appropriate timedelta format string) for datetime
        dtypes.
        """

    def var(self, *, skip_nulls: bool = True) -> DType:
        """
        Reduction returns a scalar. Must be supported for numerical and
        datetime data types. Returns a float for numerical data types, and
        datetime (with the appropriate timedelta format string) for datetime
        dtypes.
        """

    def isnull(self) -> Column:
        """
        Check for 'missing' or 'null' entries.

        Returns
        -------
        Column

        See also
        --------
        isnan

        Notes
        -----
        Does *not* include NaN-like entries.
        May optionally include 'NaT' values (if present in an implementation),
        but note that the Standard makes no guarantees about them.
        """

    def isnan(self) -> Column:
        """
        Check for nan entries.

        Returns
        -------
        Column

        See also
        --------
        isnull

        Notes
        -----
        This only checks for 'NaN'.
        Does *not* include 'missing' or 'null' entries.
        In particular, does not check for `np.timedelta64('NaT')`.
        """

    def is_in(self, values: Column) -> Column[bool]:
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

    def unique_indices(self, *, skip_nulls: bool = True) -> Column[int]:
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
