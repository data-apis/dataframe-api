__all__ = ["DataFrame"]

from typing import Sequence, TYPE_CHECKING

if TYPE_CHECKING:
    from .column_object import Column


class DataFrame:

    def get_column_by_name(self, key: str) -> Column:
        """
        Select a column by name.

        Parameters
        ----------
        key : str

        Returns
        -------
        Column

        Raises
        ------
        KeyError
            If the key is not present.
        """
        ...

    def get_columns_by_name(self, keys: Sequence[str]) -> DataFrame:
        """
        Select multiple columns by name.

        Parameters
        ----------
        keys : Sequence[str]

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
        indices.
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

    def get_rows_by_mask(self, mask: Column[bool]) -> DataFrame:
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

    def __eq__(self, other: DataFrame | "Scalar") -> DataFrame:
        """
        Parameters
        ----------
        other : DataFrame or Scalar
            If DataFrame, must have same length and matching columns.
            "Scalar" here is defined implicitly by the contained dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __ne__(self, other: DataFrame | "Scalar") -> DataFrame:
        """
        Parameters
        ----------
        other : DataFrame or Scalar
            If DataFrame, must have same length and matching columns.
            "Scalar" here is defined implicitly by the contained dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __ge__(self, other: DataFrame | "Scalar") -> DataFrame:
        """
        Parameters
        ----------
        other : DataFrame or Scalar
            If DataFrame, must have same length and matching columns.
            "Scalar" here is defined implicitly by the contained dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __gt__(self, other: DataFrame | "Scalar") -> DataFrame:
        """
        Parameters
        ----------
        other : DataFrame or Scalar
            If DataFrame, must have same length and matching columns.
            "Scalar" here is defined implicitly by the contained dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __le__(self, other: DataFrame | "Scalar") -> DataFrame:
        """
        Parameters
        ----------
        other : DataFrame or Scalar
            If DataFrame, must have same length and matching columns.
            "Scalar" here is defined implicitly by the contained dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __lt__(self, other: DataFrame | "Scalar") -> DataFrame:
        """
        Parameters
        ----------
        other : DataFrame or Scalar
            If DataFrame, must have same length and matching columns.
            "Scalar" here is defined implicitly by the contained dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __add__(self, other: DataFrame | "Scalar") -> DataFrame:
        """
        Parameters
        ----------
        other : DataFrame or Scalar
            If DataFrame, must have same length and matching columns.
            "Scalar" here is defined implicitly by the contained dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __sub__(self, other: DataFrame | "Scalar") -> DataFrame:
        """
        Parameters
        ----------
        other : DataFrame or Scalar
            If DataFrame, must have same length and matching columns.
            "Scalar" here is defined implicitly by the contained dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __mul__(self, other: DataFrame | "Scalar") -> DataFrame:
        """
        Parameters
        ----------
        other : DataFrame or Scalar
            If DataFrame, must have same length and matching columns.
            "Scalar" here is defined implicitly by the contained dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __truediv__(self, other: DataFrame | "Scalar") -> DataFrame:
        """
        Parameters
        ----------
        other : DataFrame or Scalar
            If DataFrame, must have same length and matching columns.
            "Scalar" here is defined implicitly by the contained dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __floordiv__(self, other: DataFrame | "Scalar") -> DataFrame:
        """
        Parameters
        ----------
        other : DataFrame or Scalar
            If DataFrame, must have same length and matching columns.
            "Scalar" here is defined implicitly by the contained dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __pow__(self, other: DataFrame | "Scalar") -> DataFrame:
        """
        Parameters
        ----------
        other : DataFrame or Scalar
            If DataFrame, must have same length and matching columns.
            "Scalar" here is defined implicitly by the contained dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __mod__(self, other: DataFrame | "Scalar") -> DataFrame:
        """
        Parameters
        ----------
        other : DataFrame or Scalar
            If DataFrame, must have same length and matching columns.
            "Scalar" here is defined implicitly by the contained dtypes.

        Returns
        -------
        DataFrame
        """
        ...

    def __divmod__(self, other: DataFrame | "Scalar") -> tuple[DataFrame, DataFrame]:
        """
        Parameters
        ----------
        other : DataFrame or Scalar
            If DataFrame, must have same length and matching columns.
            "Scalar" here is defined implicitly by the contained dtypes.

        Returns
        -------
        DataFrame
        DataFrame
        """
        ...
