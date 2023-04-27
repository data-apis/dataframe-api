from __future__ import annotations

from ._types import Scalar, dtype

class Column:
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
        Reduction returns a scalar.
        """

    def max(self, skip_nulls: bool = True) -> dtype:
        """
        Reduction returns a scalar.
        """

    def sum(self, skipna: bool = True) -> dtype:
        """
        Reduction returns a scalar.
        """

    def prod(self, skipna: bool = True) -> dtype:
        """
        Reduction returns a scalar.
        """

    def median(self, skipna: bool = True) -> dtype:
        """
        Reduction returns a scalar.
        """

    def mean(self, skipna: bool = True) -> dtype:
        """
        Reduction returns a scalar.
        """

    def std(self, skipna: bool = True) -> dtype:
        """
        Reduction returns a scalar.
        """

    def var(self, skipna: bool = True) -> dtype:
        """
        Reduction returns a scalar.
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
        """

    def isnan(self) -> Column:
        """
        Check for nan-like entries.

        Returns
        -------
        Column

        See also
        --------
        isnull

        Notes
        -----
        Includes anything with NaN-like semantics, e.g. np.datetime64("NaT").
        Does *not* include 'missing' or 'null' entries.
        """
