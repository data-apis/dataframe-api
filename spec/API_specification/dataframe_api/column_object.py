from __future__ import annotations

from typing import NoReturn, overload, Sequence

class Column:
    def __len__(self) -> int:
        """
        Return the number of rows.
        """
    
    @overload
    def __getitem__(self, key: int) -> object:
        ...

    @overload
    def __getitem__(self, key: Sequence[int]) -> Column:
        ...

    def __getitem__(self, key: int | Sequence[int]) -> object | Column:
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
