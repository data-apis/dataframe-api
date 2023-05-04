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
    def to_array_obj(self, *, null_handling: str | None = None) -> object:
        """
        Obtain an object that can be used as input to ``asarray`` or ``from_dlpack``

        The returned object must only be used for one thing: calling the ``asarray``
        or ``from_dlpack`` functions of a library implementing the array API
        standard, or equivalent ``asarray``/``from_dlpack`` functions to the
        one in that standard. In practice that means that the returned object
        may either already *be* an array type of a specific array library, or
        it may implement one or more of the following methods or behaviors:

        - ``__dlpack__``
        - the Python buffer protocol
        - ``__array__``
        - ``__array_interface__``
        - ``__cuda_array_interface__``
        - the Python ``Sequence`` interface
        - any other method that is known to work with an ``asarray`` function
          in a library of interest

        Importantly, the returned object must only implement/expose those
        methods that work. An ``asarray`` function may try to use any of the
        above methods, and the order in which it does so is not guaranteed.
        Hence it is expected that if a method is present, it works correctly
        and does not raise an exception (e.g., because of an unsupported dtype
        or device).

        .. admonition:: Tip

           One way to expose methods only if they will work for the dtype,
           device, and other characteristics of the column is to hide access to
           the methods dynamically, so ``hasattr`` does the right thing. For
           example::

              def __dir__(self):
                  methods = dir(self.__class__)
                  attrs = list(self.__dict__.keys())
                  keys = methods + attrs
                  if not self.dtype in _dlpack_supported_dtypes:
                      keys.remove("__dlpack__")

                  return keys

              def __dlpack__(self):
                  ...

        Parameters
        ----------
        null_handling : str or None
            Determine how to treat ``null`` values that may be present in the
            column. Valid options are:

            - ``None`` (default): no special handling. This assumes that either
              no missing values are present, or there is an array type with
              native support for missing values that is/can be converted to.
              *Note: there is currently no such library that is in wide use;
              NumPy's masked arrays are non-recommended, and other array
              libraries do not support missing values at all.*
            - ``raise``: always raise a ``ValueError`` if nulls are present.
            - ``to-nan``: for floating-point dtypes, convert any nulls to ``nan``.
              For other dtypes, do the same as ``None``.

            Note that if it is desired to convert nulls to a dtype-specific
            sentinel value, the user should do this before calling
            ``is_array_obj`` with `.isnull()` and replacing the values
            directly.

        Raises
        ------
        TypeError
            In case it is not possible to convert the column to any (known) array
            library type, or use any of the possible interchange methods.
            This can be due to the dtype (e.g., no array library supports datetime
            dtypes with a time zone), device, or other reasons.
        ValueError
            If the column contains ``null`` values which prevent returning an
            array object.

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
        Reduction returns a scalar. Must be supported for numerical and
        datetime data types. Returns a float for numerical data types, and
        datetime (with the appropriate timedelta format string) for datetime
        dtypes.
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
