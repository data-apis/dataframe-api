from __future__ import annotations

from typing import NoReturn

class Column:
    def __len__(self) -> int:
        """
        Return the number of rows.
        """
    
    def __getitem__(self, row: int) -> object:
        """
        Get the element at row index `key`.
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

    def get_rows(self, indices: Column[int]) -> Column:
        """
        Select a subset of rows, similar to `ndarray.take`.

        Parameters
        ----------
        indices : Column[int]
            Positions of rows to select.

        Returns
        -------
        Column
        """
        ...