from __future__ import annotations
from typing import Sequence, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .column_object import Column
    from .groupby_object import GroupBy
    from ._types import Scalar


__all__ = ["DataFrame"]


class DataFrame:
    def groupby(self, keys: Sequence[str], /) -> GroupBy:
        """
        Group the DataFrame by the given columns.

        Parameters
        ----------
        keys : Sequence[str]

        Returns
        -------
        GroupBy

        Raises
        ------
        KeyError
            If any of the requested keys are not present.

        Notes
        -----
        The order of the keys and the order of rows within each group is not
        guaranteed and is implementation defined.
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

    def get_columns_by_name(self, names: Sequence[str], /) -> DataFrame:
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

    def get_rows(self, indices: Sequence[int]) -> DataFrame:
        """
        Select a subset of rows, similar to `ndarray.take`.

        Parameters
        ----------
        indices : Sequence[int]
            Positions of rows to select.

        Returns
        -------
        DataFrame

        Notes
        -----
        Some discussion participants prefer a stricter type Column[int] for
        indices in order to make it easier to implement in a performant manner
        on GPUs.
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

    def get_rows_by_mask(self, mask: "Column[bool]") -> DataFrame:
        """
        Select a subset of rows corresponding to a mask.

        Parameters
        ----------
        mask : Column[bool]

        Returns
        -------
        DataFrame

        Notes
        -----
        Some participants preferred a weaker type Arraylike[bool] for mask,
        where 'Arraylike' denotes an object adhering to the Array API standard.
        """
        ...

    def insert(self, loc: int, label: str, value: Column) -> DataFrame:
        """
        Insert column into DataFrame at specified location.

        Parameters
        ----------
        loc : int
            Insertion index. Must verify 0 <= loc <= len(columns).
        label : str
            Label of the inserted column.
        value : Column
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

    def set_column(self, label: str, value: Column) -> DataFrame:
        """
        Add or replace a column.

        Parameters
        ----------
        label : str
        value : Column

        Returns
        -------
        DataFrame
        """
        ...

    def __eq__(self, other: DataFrame | Scalar) -> DataFrame:
        """
        Compare for equality.

        Parameters
        ----------
        other : DataFrame or Scalar
            If DataFrame, must have same length and matching columns.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __ne__(self, other: DataFrame | Scalar) -> DataFrame:
        """
        Compare for non-equality.

        Parameters
        ----------
        other : DataFrame or Scalar
            If DataFrame, must have same length and matching columns.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __ge__(self, other: DataFrame | Scalar) -> DataFrame:
        """
        Compare for "greater than or equal to" `other`.

        Parameters
        ----------
        other : DataFrame or Scalar
            If DataFrame, must have same length and matching columns.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __gt__(self, other: DataFrame | Scalar) -> DataFrame:
        """
        Compare for "greater than" `other`.

        Parameters
        ----------
        other : DataFrame or Scalar
            If DataFrame, must have same length and matching columns.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __le__(self, other: DataFrame | Scalar) -> DataFrame:
        """
        Compare for "less than or equal to" `other`.

        Parameters
        ----------
        other : DataFrame or Scalar
            If DataFrame, must have same length and matching columns.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __lt__(self, other: DataFrame | Scalar) -> DataFrame:
        """
        Compare for "less than" `other`.

        Parameters
        ----------
        other : DataFrame or Scalar
            If DataFrame, must have same length and matching columns.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __add__(self, other: DataFrame | Scalar) -> DataFrame:
        """
        Add `other` dataframe or scalar to this dataframe.

        Parameters
        ----------
        other : DataFrame or Scalar
            If DataFrame, must have same length and matching columns.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __sub__(self, other: DataFrame | Scalar) -> DataFrame:
        """
        Subtract `other` dataframe or scalar from this dataframe.

        Parameters
        ----------
        other : DataFrame or Scalar
            If DataFrame, must have same length and matching columns.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __mul__(self, other: DataFrame | Scalar) -> DataFrame:
        """
        Multiply  `other` dataframe or scalar with this dataframe.

        Parameters
        ----------
        other : DataFrame or Scalar
            If DataFrame, must have same length and matching columns.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __truediv__(self, other: DataFrame | Scalar) -> DataFrame:
        """
        Divide  this dataframe by `other` dataframe or scalar. True division, returns floats.

        Parameters
        ----------
        other : DataFrame or Scalar
            If DataFrame, must have same length and matching columns.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __floordiv__(self, other: DataFrame | Scalar) -> DataFrame:
        """
        Floor-divide (returns integers) this dataframe by `other` dataframe or scalar.

        Parameters
        ----------
        other : DataFrame or Scalar
            If DataFrame, must have same length and matching columns.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __pow__(self, other: DataFrame | Scalar) -> DataFrame:
        """
        Raise this dataframe to the power of `other`.

        Parameters
        ----------
        other : DataFrame or Scalar
            If DataFrame, must have same length and matching columns.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __mod__(self, other: DataFrame | Scalar) -> DataFrame:
        """
        Return modulus of this dataframe by `other` (`%` operator).

        Parameters
        ----------
        other : DataFrame or Scalar
            If DataFrame, must have same length and matching columns.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __divmod__(self, other: DataFrame | Scalar) -> tuple[DataFrame, DataFrame]:
        """
        Return quotient and remainder of integer division. See `divmod` builtin function.

        Parameters
        ----------
        other : DataFrame or Scalar
            If DataFrame, must have same length and matching columns.
            "Scalar" here is defined implicitly by what scalar types are allowed
            for the operation by the underling dtypes.

        Returns
        -------
        A tuple of two DataFrame's
        """
        ...

    def any(self, skipna: bool = True) -> DataFrame:
        """
        Reduction returns a 1-row DataFrame.
        """
        ...

    def all(self, skipna: bool = True) -> DataFrame:
        """
        Reduction returns a 1-row DataFrame.
        """
        ...

    def min(self, skipna: bool = True) -> DataFrame:
        """
        Reduction returns a 1-row DataFrame.
        """
        ...

    def max(self, skipna: bool = True) -> DataFrame:
        """
        Reduction returns a 1-row DataFrame.
        """
        ...

    def sum(self, skipna: bool = True) -> DataFrame:
        """
        Reduction returns a 1-row DataFrame.
        """
        ...

    def prod(self, skipna: bool = True) -> DataFrame:
        """
        Reduction returns a 1-row DataFrame.
        """
        ...

    def median(self, skipna: bool = True) -> DataFrame:
        """
        Reduction returns a 1-row DataFrame.
        """
        ...

    def mean(self, skipna: bool = True) -> DataFrame:
        """
        Reduction returns a 1-row DataFrame.
        """
        ...

    def std(self, skipna: bool = True) -> DataFrame:
        """
        Reduction returns a 1-row DataFrame.
        """
        ...

    def var(self, skipna: bool = True) -> DataFrame:
        """
        Reduction returns a 1-row DataFrame.
        """
        ...

    def isnull(self) -> DataFrame:
        """
        Check for 'missing' or 'null' entries.

        Returns
        -------
        DataFrame

        See also
        --------
        isnan

        Notes
        -----
        Does *not* include NaN-like entries.
        """
        ...

    def isnan(self) -> DataFrame:
        """
        Check for nan-like entries.

        Returns
        -------
        DataFrame

        See also
        --------
        isnull

        Notes
        -----
        Includes anything with NaN-like semantics, e.g. np.datetime64("NaT").
        Does *not* include 'missing' or 'null' entries.
        """
        ...
