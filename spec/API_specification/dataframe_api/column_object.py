from typing import NoReturn

class Column:
    def __len__(self) -> int:
        """
        Return the number of rows.
        """
    
    def __getitem__(self, row: int) -> object:
        """
        Get the element at row index `row`.
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
