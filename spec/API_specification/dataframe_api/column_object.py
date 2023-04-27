from __future__ import annotations

from typing import Sequence

from ._types import Scalar, dtype


__all__ = ['Column']


class Column:
    """
    Column object

    Note that this column object is not meant to be instantiated directly by
    users of the library implementing the dataframe API standard. Rather, use
    constructor functions or an already-created dataframe object retrieved via

    """
    @classmethod
    def from_sequence(cls, sequence: Sequence[object], dtype: dtype) -> Column:
        """
        Construct Column from sequence of elements.

        Parameters
        ----------
        sequence : Sequence[object]
            Sequence of elements. Each element must be of the specified
            ``dtype``, the corresponding Python builtin scalar type, or
            coercible to that Python scalar type.
        dtype : str
            Dtype of result. Must be specified.
        
        Returns
        -------
        Column
        """

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

    def __and__(self, other: Column | Scalar) -> Column:
        """
        Add `other` dataframe or scalar to this column.

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
        Subtract `other` dataframe or scalar from this column.

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
        Multiply `other` dataframe or scalar with this column.

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
        Floor-divide `other` dataframe or scalar to this column.

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

    def any(self, skip_nulls: bool = True) -> bool:
        """
        Reduction returns a bool.

        Raises
        ------
        ValueError
            If column is not boolean.
        """

    def all(self, skip_nulls: bool = True) -> bool:
        """
        Reduction returns a bool.

        Raises
        ------
        ValueError
            If column is not boolean.
        """

    def min(self, skip_nulls: bool = True) -> dtype:
        """
        Reduction returns a scalar. Any data type that supports comparisons
        must be supported. The returned value has the same dtype as the column.
        """

    def max(self, skip_nulls: bool = True) -> dtype:
        """
        Reduction returns a scalar. Any data type that supports comparisons
        must be supported. The returned value has the same dtype as the column.
        """

    def sum(self, skip_nulls: bool = True) -> dtype:
        """
        Reduction returns a scalar. Must be supported for numerical and
        datetime data types. The returned value has the same dtype as the
        column.
        """

    def prod(self, skip_nulls: bool = True) -> dtype:
        """
        Reduction returns a scalar. Must be supported for numerical data types.
        The returned value has the same dtype as the column.
        """

    def median(self, skip_nulls: bool = True) -> dtype:
        """
        Reduction returns a scalar. Any data type that supports comparisons
        must be supported. The returned value has the same dtype as the column.
        """

    def mean(self, skip_nulls: bool = True) -> dtype:
        """
        Reduction returns a scalar. Must be supported for numerical and
        datetime data types. Returns a float for numerical data types, and
        datetime (with the appropriate timedelta format string) for datetime
        dtypes.
        """

    def std(self, skip_nulls: bool = True) -> dtype:
        """
        Reduction returns a scalar. Must be supported for numerical and
        datetime data types. Returns a float for numerical data types, and
        datetime (with the appropriate timedelta format string) for datetime
        dtypes.
        """

    def var(self, skip_nulls: bool = True) -> dtype:
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