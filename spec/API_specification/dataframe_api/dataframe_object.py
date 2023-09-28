from __future__ import annotations

from typing import Any, Literal, Mapping, Sequence, Union, TYPE_CHECKING, NoReturn


if TYPE_CHECKING:
    from .column_object import Column
    from .groupby_object import GroupBy
    from ._types import NullType, Scalar, Namespace, DType


__all__ = ["DataFrame"]


class DataFrame:
    """
    DataFrame object

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
        """
        Returns an object that has all the top-level dataframe API functions on it.

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
    def dataframe(self) -> object:
        """
        Return underlying (not-necessarily-Standard-compliant) DataFrame.

        If a library only implements the Standard, then this can return `self`.
        """
        ...
    
    def shape(self) -> tuple[int, int]:
        """
        Return number of rows and number of columns.
        """

    def group_by(self, keys: str | list[str], /) -> GroupBy:
        """
        Group the DataFrame by the given columns.

        Parameters
        ----------
        keys : str | list[str]

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

    def get_column_by_name(self, name: str, /) -> Column:
        """
        Select a column by name.

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

    def select(self, names: Sequence[str], /) -> DataFrame:
        """
        Select multiple columns by name.

        Parameters
        ----------
        names : Sequence[str]

        Returns
        -------
        DataFrame

        Raises
        ------
        KeyError
            If the any requested key is not present.
        """
        ...

    def get_rows(self, indices: Column) -> DataFrame:
        """
        Select a subset of rows, similar to `ndarray.take`.

        Parameters
        ----------
        indices : Column
            Positions of rows to select.

        Returns
        -------
        DataFrame
        """
        ...

    def slice_rows(
        self, start: int | None, stop: int | None, step: int | None
    ) -> DataFrame:
        """
        Select a subset of rows corresponding to a slice.

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

    def filter(self, mask: Column) -> DataFrame:
        """
        Select a subset of rows corresponding to a mask.

        Parameters
        ----------
        mask : Column

        Returns
        -------
        DataFrame

        Notes
        -----
        Some participants preferred a weaker type Arraylike[bool] for mask,
        where 'Arraylike' denotes an object adhering to the Array API standard.
        """
        ...

    def insert_column(self, column: Column) -> DataFrame:
        """
        Insert column into DataFrame at rightmost location.

        The column's name will be used as the label in the resulting dataframe.
        To insert the column with a different name, combine with `Column.rename`,
        e.g.:

        .. code-block:: python

            new_column = df.get_column_by_name('a') + 1
            df = df.insert_column(new_column.rename('a_plus_1'))
        
        If you need to insert the column at a different location, combine with
        :meth:`select`, e.g.:

        .. code-block:: python

            new_column = df.get_column_by_name('a') + 1
            new_columns_names = ['a_plus_1'] + df.column_names
            df = df.insert_column(new_column.rename('a_plus_1'))
            df = df.select(new_column_names)

        Parameters
        ----------
        column : Column
        """
        ...

    def update_columns(self, columns: Column | Sequence[Column], /) -> DataFrame:
        """
        Update values in existing column(s) from Dataframe.

        The column's name will be used to tell which column to update.
        To update a column with a different name, combine with :meth:`Column.rename`,
        e.g.:

        .. code-block:: python

            new_column = df.get_column_by_name('a') + 1
            df = df.update_column(new_column.rename('b'))

        Parameters
        ----------
        columns : Column | Sequence[Column]
            Column(s) to update. If updating multiple columns, they must all have
            different names.

        Returns
        -------
        DataFrame
        """
        ...

    def drop_column(self, label: str) -> DataFrame:
        """
        Drop the specified column.

        Parameters
        ----------
        label : str

        Returns
        -------
        DataFrame

        Raises
        ------
        KeyError
            If the label is not present.
        """
        ...

    def rename_columns(self, mapping: Mapping[str, str]) -> DataFrame:
        """
        Rename columns.

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
        """
        Get column names.

        Returns
        -------
        list[str]
        """
        ...
    
    @property
    def schema(self) -> dict[str, Any]:
        """
        Get dataframe's schema.

        Returns
        -------
        dict[str, Any]
            Mapping from column name to data type.
        """
    
    def sort(
        self,
        keys: str | list[str] | None = None,
        *,
        ascending: Sequence[bool] | bool = True,
        nulls_position: Literal['first', 'last'] = 'last',
    ) -> DataFrame:
        """
        Sort dataframe according to given columns.

        If you only need the indices which would sort the dataframe, use
        :meth:`sorted_indices`.

        Parameters
        ----------
        keys : str | list[str], optional
            Names of columns to sort by.
            If `None`, sort by all columns.
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

    def sorted_indices(
        self,
        keys: str | list[str] | None = None,
        *,
        ascending: Sequence[bool] | bool = True,
        nulls_position: Literal['first', 'last'] = 'last',
    ) -> Column:
        """
        Return row numbers which would sort according to given columns.

        If you need to sort the DataFrame, use :meth:`sort`.

        Parameters
        ----------
        keys : str | list[str], optional
            Names of columns to sort by.
            If `None`, sort by all columns.
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
        Column
    
        Raises
        ------
        ValueError
            If `keys` and `ascending` are sequences of different lengths.
        """
        ...

    def __eq__(self, other: Scalar) -> DataFrame:  # type: ignore[override]
        """
        Compare for equality.

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

    def __ne__(self, other: Scalar) -> DataFrame:  # type: ignore[override]
        """
        Compare for non-equality.

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

    def __ge__(self, other: Scalar) -> DataFrame:
        """
        Compare for "greater than or equal to" `other`.

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

    def __gt__(self, other: Scalar) -> DataFrame:
        """
        Compare for "greater than" `other`.

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

    def __le__(self, other: Scalar) -> DataFrame:
        """
        Compare for "less than or equal to" `other`.

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

    def __lt__(self, other: Scalar) -> DataFrame:
        """
        Compare for "less than" `other`.

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

    def __and__(self, other: bool) -> DataFrame:
        """
        Apply logical 'and' to `other` scalar and this dataframe.

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

    def __or__(self, other: DataFrame | bool) -> DataFrame:
        """
        Apply logical 'or' to `other` scalar and this DataFrame.

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

    def __add__(self, other: Scalar) -> DataFrame:
        """
        Add `other` scalar to this dataframe.

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

    def __sub__(self, other: Scalar) -> DataFrame:
        """
        Subtract `other` scalar from this dataframe.

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

    def __mul__(self, other: Scalar) -> DataFrame:
        """
        Multiply  `other` scalar with this dataframe.

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

    def __truediv__(self, other: Scalar) -> DataFrame:
        """
        Divide  this dataframe by `other` scalar. True division, returns floats.

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

    def __floordiv__(self, other: Scalar) -> DataFrame:
        """
        Floor-divide (returns integers) this dataframe by `other` scalar.

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

    def __pow__(self, other: Scalar) -> DataFrame:
        """
        Raise this dataframe to the power of `other`.

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

    def __mod__(self, other: Scalar) -> DataFrame:
        """
        Return modulus of this dataframe by `other` (`%` operator).

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

    def __divmod__(self, other: Scalar) -> tuple[DataFrame, DataFrame]:
        """
        Return quotient and remainder of integer division. See `divmod` builtin function.

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

    def __invert__(self) -> DataFrame:
        """
        Invert truthiness of (boolean) elements.

        Raises
        ------
        ValueError
            If any of the DataFrame's columns is not boolean.
        """
        ...

    def __iter__(self) -> NoReturn:
        """
        Iterate over elements.

        This is intentionally "poisoned" to discourage inefficient code patterns.

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError("'__iter__' is intentionally not implemented.")

    def any(self, *, skip_nulls: bool = True) -> DataFrame:
        """
        Reduction returns a 1-row DataFrame.

        Raises
        ------
        ValueError
            If any of the DataFrame's columns is not boolean.
        """
        ...

    def all(self, *, skip_nulls: bool = True) -> DataFrame:
        """
        Reduction returns a 1-row DataFrame.

        Raises
        ------
        ValueError
            If any of the DataFrame's columns is not boolean.
        """
        ...
    
    def any_rowwise(self, *, skip_nulls: bool = True) -> Column:
        """
        Reduction returns a Column.

        Differs from ``DataFrame.any`` and that the reduction happens
        for each row, rather than for each column.

        Raises
        ------
        ValueError
            If any of the DataFrame's columns is not boolean.
        """
        ...

    def all_rowwise(self, *, skip_nulls: bool = True) -> Column:
        """
        Reduction returns a Column.

        Differs from ``DataFrame.all`` and that the reduction happens
        for each row, rather than for each column.

        Raises
        ------
        ValueError
            If any of the DataFrame's columns is not boolean.
        """
        ...

    def min(self, *, skip_nulls: bool = True) -> DataFrame:
        """
        Reduction returns a 1-row DataFrame.
        """
        ...

    def max(self, *, skip_nulls: bool = True) -> DataFrame:
        """
        Reduction returns a 1-row DataFrame.
        """
        ...

    def sum(self, *, skip_nulls: bool = True) -> DataFrame:
        """
        Reduction returns a 1-row DataFrame.
        """
        ...

    def prod(self, *, skip_nulls: bool = True) -> DataFrame:
        """
        Reduction returns a 1-row DataFrame.
        """
        ...

    def median(self, *, skip_nulls: bool = True) -> DataFrame:
        """
        Reduction returns a 1-row DataFrame.
        """
        ...

    def mean(self, *, skip_nulls: bool = True) -> DataFrame:
        """
        Reduction returns a 1-row DataFrame.
        """
        ...

    def std(self, *, correction: int | float = 1, skip_nulls: bool = True) -> DataFrame:
        """
        Reduction returns a 1-row DataFrame.

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

    def var(self, *, correction: int | float = 1, skip_nulls: bool = True) -> DataFrame:
        """
        Reduction returns a 1-row DataFrame.

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

    def is_null(self) -> DataFrame:
        """
        Check for 'missing' or 'null' entries.

        Returns
        -------
        DataFrame

        See also
        --------
        is_nan

        Notes
        -----
        Does *not* include NaN-like entries.
        May optionally include 'NaT' values (if present in an implementation),
        but note that the Standard makes no guarantees about them.
        """
        ...

    def is_nan(self) -> DataFrame:
        """
        Check for nan entries.

        Returns
        -------
        DataFrame

        See also
        --------
        is_null

        Notes
        -----
        This only checks for 'NaN'.
        Does *not* include 'missing' or 'null' entries.
        In particular, does not check for `np.timedelta64('NaT')`.
        """
        ...

    def unique_indices(self, keys: str | list[str] | None = None, *, skip_nulls: bool = True) -> Column:
        """
        Return indices corresponding to unique values across selected columns.

        Parameters
        ----------
        keys : str | list[str], optional
            Column names to consider when finding unique values.
            If `None`, all columns are considered.

        Returns
        -------
        Column
            Indices corresponding to unique values.

        Notes
        -----
        There are no ordering guarantees. In particular, if there are multiple
        indices corresponding to the same unique value(s), there is no guarantee
        about which one will appear in the result.
        If the original column(s) contain multiple `'NaN'` values, then
        only a single index corresponding to those values will be returned.
        Likewise for null values (if ``skip_nulls=False``).
        To get the unique values, you can do ``df.get_rows(df.unique_indices(keys))``.
        """
        ...

    def fill_nan(self, value: float | NullType, /) -> DataFrame:
        """
        Fill ``nan`` values with the given fill value.

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
        self, value: Scalar, /, *, column_names : list[str] | None = None
    ) -> DataFrame:
        """
        Fill null values with the given fill value.

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
    
    def to_array_object(self, dtype: DType) -> Any:
        """
        Convert to array-API-compliant object.

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
        other: DataFrame,
        *,
        how: Literal['left', 'inner', 'outer'],
        left_on: str | list[str],
        right_on: str | list[str],
    ) -> DataFrame:
        """
        Join with other dataframe.

        Other than the joining column name(s), no column name is allowed to appear in
        both `self` and `other`. Rename columns before calling `join` if necessary
        using :meth:`rename_columns`.

        Parameters
        ----------
        other : DataFrame
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
