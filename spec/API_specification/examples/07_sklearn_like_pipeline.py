"""Scikit-learn-like pipeline.

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

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from typing_extensions import Self

    from dataframe_api.typing import Column, DataFrame, Scalar


class Scaler:
    """Apply a standardization scaling factor to `column_names`."""

    scalings_: dict[str, Scalar]

    def __init__(self, column_names: list[str]) -> None:
        self.column_names = column_names

    def fit(self, df: DataFrame) -> Self:
        """Compute scaling factors from given data frame.

        A typical data science workflow is to fit on one dataset,
        and then transform and multiple datasets. Therefore, we
        make sure to `persist` within the `fit` method.
        """
        scalings = df.select(*self.column_names).std().persist()

        self.scalings_ = {
            column_name: scalings.col(column_name).get_value(0)
            for column_name in self.column_names
        }

        return self

    def transform(self, df: DataFrame) -> DataFrame:
        """Apply the "trained" scaling values.

        This function is guaranteed to not collect values.
        """
        columns: list[Column] = []
        for column_name in df.column_names:
            if column_name not in self.column_names:
                continue
            column = df.col(column_name) / self.scalings_[column_name]
            columns.append(column)

        # Note: `assign` is not in-place
        return df.assign(*columns)


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
        # Note: This assumes that select ensures the column order.
        return df.select(*self.columns_)


class Pipeline:
    """Linear pipeline of transformers."""

    def __init__(self, steps: list[Any]) -> None:
        self.steps = steps

    def fit(self, df: DataFrame) -> Self:
        """Call fit on the steps of the pipeline subsequently.

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
