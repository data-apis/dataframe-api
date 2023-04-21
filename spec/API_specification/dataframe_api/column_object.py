from __future__ import annotations

from typing import Sequence

class Column:
    def unique(self) -> Column:
        """
        Return a Column with a row for each unique value.

        Returns
        -------
        Column

        Notes
        -----
        There are no ordering guarantees.
        """
        ...
