from __future__ import annotations

from typing import Sequence

from ._types import dtype


__all__ = ['Column']


class Column:
    """
    Column object

    Note that this column object is not meant to be instantiated directly by
    users of the library implementing the dataframe API standard. Rather, use
    constructor functions or an already-created dataframe object retrieved via

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
