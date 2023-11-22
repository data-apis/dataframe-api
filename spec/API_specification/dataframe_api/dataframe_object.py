from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, NoReturn, Protocol

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from typing_extensions import Self

    from .column_object import Column
    from .groupby_object import GroupBy
    from .typing import (
        AnyScalar,
        DType,
        Namespace,
        NullType,
        Scalar,
        SupportsDataFrameAPI,
    )


__all__ = ["DataFrame"]


class DataFrame(Protocol):
    """DataFrame object.

    Note that this dataframe object is not meant to be instantiated directly by
    users of the library implementing the dataframe API standard. Rather, use
    constructor functions or an already-created dataframe object retrieved via

    **Python operator support**

    All arithmetic operators defined by the Python language, except for
    ``__matmul__``, ``__neg__`` and ``__pos__``, must be supported for
    numerical data types.

    All comparison operators defined by the Python language must be supported
    by the dataframe object for all data types for which those comparisons are
    supported by the builtin scalar types corresponding to a data type.

    In-place operators must not be supported. All operations on the dataframe
    object are out-of-place.

    **Methods and Attributes**

    """

    def __dataframe_namespace__(self) -> Namespace:
        """Return an object that has all the top-level dataframe API functions on it.

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
    def dataframe(self) -> SupportsDataFrameAPI:
        """Return underlying (not-necessarily-Standard-compliant) DataFrame.

        If a library only implements the Standard, then this can return `self`.
        """
        ...

    def shape(self) -> tuple[int, int]:
        """Return number of rows and number of columns."""
        ...

    def group_by(self, *keys: str) -> GroupBy:
        """Group the DataFrame by the given columns.

        Parameters
        ----------
        *keys : str

        Returns
        -------
        GroupBy

        Raises
        ------
        KeyError
            If any of the requested keys are not present.

        Notes
        -----
        Downstream operations from this function, like aggregations, return
        results for which row order is not guaranteed and is implementation
        defined.
        """
        ...

    def col(self, name: str, /) -> Column:
        """Select a column by name.

        Parameters
        ----------
        name : str

        Returns
        -------
        Column

        Raises
        ------
        KeyError
            If the key is not present.
        """
        ...

    def select(self, *names: str) -> Self:
        """Select multiple columns by name.

        Parameters
        ----------
        *names : str

        Returns
        -------
        DataFrame

        Raises
        ------
        KeyError
            If the any requested key is not present.
        """
        ...

    def get_rows(self, indices: Column) -> Self:
        """Select a subset of rows, similar to `ndarray.take`.

        Parameters
        ----------
        indices : Column
            Positions of rows to select.

        Returns
        -------
        DataFrame

        Notes
        -----
        `indices`'s parent DataFrame must be `self` - else,
        the operation is unsupported and may vary across implementations.
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
        DataFrame
        """
        ...

    def filter(self, mask: Column) -> Self:
        """Select a subset of rows corresponding to a mask.

        Parameters
        ----------
        mask : Column

        Returns
        -------
        DataFrame

        Notes
        -----
        `mask`'s parent DataFrame must be `self` - else,
        the operation is unsupported and may vary across implementations.
        """
        ...

    def assign(self, *columns: Column) -> Self:
        """Insert new column(s), or update values in existing ones.

        If inserting new columns, the column's names will be used as the labels,
        and the columns will be inserted at the rightmost location.

        If updating existing columns, their names will be used to tell which columns
        to update. To update a column with a different name, combine with
        :meth:`Column.rename`, e.g.:

        .. code-block:: python

            new_column = df.col('a') + 1
            df = df.assign(new_column.rename('b'))

        Parameters
        ----------
        *columns : Column
            Column(s) to update/insert. If updating/inserting multiple columns,
            they must all have different names.

        Returns
        -------
        DataFrame

        Notes
        -----
        All of `columns`'s parent DataFrame must be `self` - else,
        the operation is unsupported and may vary across implementations.
        """
        ...

    def drop_columns(self, *labels: str) -> Self:
        """Drop the specified column(s).

        Parameters
        ----------
        *label : str
            Column name(s) to drop.

        Returns
        -------
        DataFrame

        Raises
        ------
        KeyError
            If the label is not present.
        """
        ...

    def rename_columns(self, mapping: Mapping[str, str]) -> Self:
        """Rename columns.

        Parameters
        ----------
        mapping : Mapping[str, str]
            Keys are old column names, values are new column names.

        Returns
        -------
        DataFrame
        """
        ...

    @property
    def column_names(self) -> list[str]:
        """Get column names.

        Returns
        -------
        list[str]
        """
        ...

    @property
    def schema(self) -> dict[str, DType]:
        """Get dataframe's schema.

        Returns
        -------
        dict[str, Any]
            Mapping from column name to data type.
        """
        ...

    def sort(
        self,
        *keys: str,
        ascending: Sequence[bool] | bool = True,
        nulls_position: Literal["first", "last"] = "last",
    ) -> Self:
        """Sort dataframe according to given columns.

        If you only need the indices which would sort the dataframe, use
        `sorted_indices`.

        Parameters
        ----------
        *keys : str
            Names of columns to sort by.
            If not specified, sort by all columns.
        ascending : Sequence[bool] or bool
            If `True`, sort by all keys in ascending order.
            If `False`, sort by all keys in descending order.
            If a sequence, it must be the same length as `keys`,
            and determines the direction with which to use each
            key to sort by.
        nulls_position : ``{'first', 'last'}``
            Whether null values should be placed at the beginning
            or at the end of the result.
            Note that the position of NaNs is unspecified and may
            vary based on the implementation.

        Returns
        -------
        DataFrame

        Raises
        ------
        ValueError
            If `keys` and `ascending` are sequences of different lengths.
        """
        ...

    def __eq__(self, other: AnyScalar) -> Self:  # type: ignore[override]
        """Compare for equality.

        Nulls should follow Kleene Logic.

        Parameters
        ----------
        other : Scalar
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __ne__(self, other: AnyScalar) -> Self:  # type: ignore[override]
        """Compare for non-equality.

        Nulls should follow Kleene Logic.

        Parameters
        ----------
        other : Scalar
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __ge__(self, other: AnyScalar) -> Self:
        """Compare for "greater than or equal to" `other`.

        Parameters
        ----------
        other : Scalar
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __gt__(self, other: AnyScalar) -> Self:
        """Compare for "greater than" `other`.

        Parameters
        ----------
        other : Scalar
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __le__(self, other: AnyScalar) -> Self:
        """Compare for "less than or equal to" `other`.

        Parameters
        ----------
        other : Scalar
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __lt__(self, other: AnyScalar) -> Self:
        """Compare for "less than" `other`.

        Parameters
        ----------
        other : Scalar
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __and__(self, other: bool) -> Self:  # noqa: FBT001
        """Apply logical 'and' to `other` scalar and this dataframe.

        Nulls should follow Kleene Logic.

        Parameters
        ----------
        other : bool

        Returns
        -------
        DataFrame[bool]

        Raises
        ------
        ValueError
            If `self` or `other` is not boolean.
        """
        ...

    def __or__(self, other: bool) -> Self:  # noqa: FBT001
        """Apply logical 'or' to `other` scalar and this DataFrame.

        Nulls should follow Kleene Logic.

        Parameters
        ----------
        other : bool

        Returns
        -------
        DataFrame[bool]

        Raises
        ------
        ValueError
            If `self` or `other` is not boolean.
        """
        ...

    def __add__(self, other: AnyScalar) -> Self:
        """Add `other` scalar to this dataframe.

        Parameters
        ----------
        other : Scalar
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __sub__(self, other: AnyScalar) -> Self:
        """Subtract `other` scalar from this dataframe.

        Parameters
        ----------
        other : Scalar
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __mul__(self, other: AnyScalar) -> Self:
        """Multiply  `other` scalar with this dataframe.

        Parameters
        ----------
        other : Scalar
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __truediv__(self, other: AnyScalar) -> Self:
        """Divide  this dataframe by `other` scalar. True division, returns floats.

        Parameters
        ----------
        other : Scalar
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __floordiv__(self, other: AnyScalar) -> Self:
        """Floor-divide (returns integers) this dataframe by `other` scalar.

        Parameters
        ----------
        other : Scalar
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __pow__(self, other: AnyScalar) -> Self:
        """Raise this dataframe to the power of `other`.

        Integer dtype to the power of non-negative integer dtype is integer dtype.
        Integer dtype to the power of float dtype is float dtype.
        Float dtype to the power of integer dtype or float dtype is float dtype.

        Parameters
        ----------
        other : Scalar
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __mod__(self, other: AnyScalar) -> Self:
        """Return modulus of this dataframe by `other` (`%` operator).

        Parameters
        ----------
        other : Scalar
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __divmod__(self, other: AnyScalar) -> tuple[DataFrame, DataFrame]:
        """Return quotient and remainder of integer division. See `divmod` builtin.

        Parameters
        ----------
        other : Scalar
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        A tuple of two `DataFrame`s
        """
        ...

    def __radd__(self, other: AnyScalar) -> Self:
        ...

    def __rsub__(self, other: AnyScalar) -> Self:
        ...

    def __rmul__(self, other: AnyScalar) -> Self:
        ...

    def __rtruediv__(self, other: AnyScalar) -> Self:
        ...

    def __rand__(self, other: AnyScalar) -> Self:
        ...

    def __ror__(self, other: AnyScalar) -> Self:
        ...

    def __rfloordiv__(self, other: AnyScalar) -> Self:
        ...

    def __rpow__(self, other: AnyScalar) -> Self:
        ...

    def __rmod__(self, other: AnyScalar) -> Self:
        ...

    def __invert__(self) -> Self:
        """Invert truthiness of (boolean) elements.

        Raises
        ------
        ValueError
            If any of the DataFrame's columns is not boolean.
        """
        ...

    def __iter__(self) -> NoReturn:
        """Iterate over elements.

        This is intentionally "poisoned" to discourage inefficient code patterns.

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError("'__iter__' is intentionally not implemented.")

    def any(self, *, skip_nulls: bool | Scalar = True) -> Self:
        """Reduction returns a 1-row DataFrame.

        Raises
        ------
        ValueError
            If any of the DataFrame's columns is not boolean.
        """
        ...

    def all(self, *, skip_nulls: bool | Scalar = True) -> Self:
        """Reduction returns a 1-row DataFrame.

        Raises
        ------
        ValueError
            If any of the DataFrame's columns is not boolean.
        """
        ...

    def min(self, *, skip_nulls: bool | Scalar = True) -> Self:
        """Reduction returns a 1-row DataFrame."""
        ...

    def max(self, *, skip_nulls: bool | Scalar = True) -> Self:
        """Reduction returns a 1-row DataFrame."""
        ...

    def sum(self, *, skip_nulls: bool | Scalar = True) -> Self:
        """Reduction returns a 1-row DataFrame."""
        ...

    def prod(self, *, skip_nulls: bool | Scalar = True) -> Self:
        """Reduction returns a 1-row DataFrame."""
        ...

    def median(self, *, skip_nulls: bool | Scalar = True) -> Self:
        """Reduction returns a 1-row DataFrame."""
        ...

    def mean(self, *, skip_nulls: bool | Scalar = True) -> Self:
        """Reduction returns a 1-row DataFrame."""
        ...

    def std(
        self,
        *,
        correction: float | Scalar = 1,
        skip_nulls: bool | Scalar = True,
    ) -> Self:
        """Reduction returns a 1-row DataFrame.

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

    def var(
        self,
        *,
        correction: float | Scalar = 1,
        skip_nulls: bool | Scalar = True,
    ) -> Self:
        """Reduction returns a 1-row DataFrame.

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

    def is_null(self) -> Self:
        """Check for 'missing' or 'null' entries.

        Returns
        -------
        DataFrame

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
        DataFrame

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

    def fill_nan(self, value: float | NullType | Scalar, /) -> Self:
        """Fill ``nan`` values with the given fill value.

        The fill operation will apply to all columns with a floating-point
        dtype. Other columns remain unchanged.

        Parameters
        ----------
        value : float or `null`
            Value used to replace any ``nan`` in the column with. Must be
            of the Python scalar type matching the dtype of the column (or
            be `null`).

        """
        ...

    def fill_null(
        self,
        value: AnyScalar,
        /,
        *,
        column_names: list[str] | None = None,
    ) -> Self:
        """Fill null values with the given fill value.

        This method can only be used if all columns that are to be filled are
        of the same dtype (e.g., all of ``Float64`` or all of string dtype).
        If that is not the case, it is not possible to use a single Python
        scalar type that matches the dtype of all columns to which
        ``fill_null`` is being applied, and hence an exception will be raised.

        Parameters
        ----------
        value : Scalar
            Value used to replace any ``null`` values in the dataframe with.
            Must be of the Python scalar type matching the dtype(s) of the dataframe.
        column_names : list[str] | None
            A list of column names for which to replace nulls with the given
            scalar value. If ``None``, nulls will be replaced in all columns.

        Raises
        ------
        TypeError
            If the columns of the dataframe are not all of the same kind.
        KeyError
            If ``column_names`` contains a column name that is not present in
            the dataframe.

        """
        ...

    def drop_nulls(
        self,
        *,
        column_names: list[str] | None = None,
    ) -> Self:
        """Drop rows containing null values.

        Parameters
        ----------
        column_names : list[str] | None
            A list of column names to consider when dropping nulls.
            If ``None``, all columns will be considered.

        Raises
        ------
        KeyError
            If ``column_names`` contains a column name that is not present in
            the dataframe.

        """
        ...

    def to_array(self, dtype: DType) -> Any:
        """Convert to array-API-compliant object.

        Parameters
        ----------
        dtype : DType
            The dtype of the array-API-compliant object to return.
            Must be one of:

            - Bool()
            - Int8()
            - Int16()
            - Int32()
            - Int64()
            - UInt8()
            - UInt16()
            - UInt32()
            - UInt64()
            - Float32()
            - Float64()

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

    def join(
        self,
        other: Self,
        *,
        how: Literal["left", "inner", "outer"],
        left_on: str | list[str],
        right_on: str | list[str],
    ) -> Self:
        """Join with other dataframe.

        Other than the joining column name(s), no column name is allowed to appear in
        both `self` and `other`. Rename columns before calling `join` if necessary
        using :meth:`rename_columns`.

        Parameters
        ----------
        other : Self
            Dataframe to join with.
        how : str
            Kind of join to perform.
            Must be one of {'left', 'inner', 'outer'}.
        left_on : str | list[str]
            Key(s) from `self` to perform `join` on.
            If more than one key is given, it must be
            the same length as `right_on`.
        right_on : str | list[str]
            Key(s) from `other` to perform `join` on.
            If more than one key is given, it must be
            the same length as `left_on`.

        Returns
        -------
        DataFrame

        Raises
        ------
        ValueError
            If, apart from `left_on` and `right_on`, there are any column names
            present in both `self` and `other`.
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

            For example, do this

            .. code-block:: python

                df: DataFrame
                features = []
                result = df.std() > 0
                result = result.persist()
                for column_name in df.column_names:
                    if result.col(column_name).get_value(0):
                        features.append(column_name)

            instead of this:

            .. code-block:: python

                df: DataFrame
                features = []
                for column_name in df.column_names:
                    # Do NOT call `persist` on a `DataFrame` within a for-loop!
                    # This may re-trigger the same computation multiple times
                    if df.persist().col(column_name).std() > 0:
                        features.append(column_name)
        """
        ...
