"""
This is an example of how a (possibly) lazy data frame may be used
in a sklearn-like pipeline.

The example is motivated by the prospect of a fully lazy, ONNX-based
data frame implementation. The concept is that calls to `fit` are
eager. They compute some state that is later meant to be transferred
into the ONNX graph/model. That transfer happens when calling
`transform`. The logic within the `transform` methods is "traced"
lazily and the resulting lazy object is then exported to ONNX.
""" 
from __future__ import annotations

from typing import Any, TYPE_CHECKING, Self

from dataframe_api.dataframe_object import DataFrame

#: Dummy type alias for a standard compliant array object
Array = Any


class Scaler:
    """Apply a standardization scaling factor to `column_names`."""    
    scalings_: dict[str, float]

    def __init__(self, column_names: list[str]):
        self.column_names = column_names

    def fit(self, df: DataFrame) -> Self:
        """Compute scaling factors from given data frame.

        Calling this function requires collecting values.
        """
        self.scalings_ = {}
        for column_name in df.column_names:
            if not column_name in self.column_names:
                continue
            self.scalings_[column_name] = df.get_column_by_name(column_name).std()

        return self

    def transform(self, df: DataFrame) -> DataFrame:
        """Apply the "trained" scaling values.

        This function is guaranteed to not collect values.
        """
        df = copy_df(df)
        for column_name in df.column_names:
            if not column_name in self.column_names:
                continue
            column = df.get_column_by_name(column_name) / self.scalings_[column_name]
            df.assign(column)

        return df

class FeatureSelector:
    """Limit columns to those seen in training including their order."""

    def fit(self, df: DataFrame) -> Self:
        """Record the observed columns and their order.

        This function is guaranteed to not collect values.
        """
        self.columns_ = df.column_names
        return self

    def transform(self, df: DataFrame) -> DataFrame:
        """Select and sort the columns as observed in training.

        This function is guaranteed to not collect values.
        """
        # FIXME: Does this ensure column order?
        return df.select(self.columns_)


class Pipeline:
    """Linear pipeline of transformers."""

    def __init__(self, steps: list[Any]):
        self.steps = steps
    
    def fit(self, df: DataFrame) -> Self:
        """Call filt on the steps of the pipeline subsequently.

        Calling this function may trigger a collection.
        """
        for step in self.steps:
            step.fit(df)

        self.steps_ = self.steps
        return self

    def transform(self, df: DataFrame) -> DataFrame:
        """Call transform on all steps of this pipeline subsequently.

        This function is guaranteed to not trigger a collection.
        """
        for step in self.steps_:
            df = step.transform(df)

        return df


def copy_df(df: DataFrame):
    """Create a copy of `df`.

    This is done by converting a data frame into standard-arrays and
    assembling them back into a new data frame.
    """
    dfx = df.__dataframe_namespace__()

    dct = dataframe_to_dict_of_arrays(df)
    return dfx.dataframe_from_dict(
        # FIXME: This would require some kind of dtype mapping?
        {column_name: dfx.column_from_1d_array(arr, dtype=arr.dtype) for column_name, arr in dct.items()}
    )


def dataframe_to_dict_of_arrays(df: DataFrame) -> dict[str, Array]:
    """Convert the given data frame into an dictionary of standard arrays. """
    dct = {}
    dfx = df.__dataframe_namespace__()
    for column_name in df.column_names:
        column = df.get_column_by_name(column_name)
        dct[column_name] = column.to_array_object(column.dtype)

    return dct
