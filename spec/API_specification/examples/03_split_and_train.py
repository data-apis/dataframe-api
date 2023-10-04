from __future__ import annotations

from dataframe_api import DataFrame

from typing import Callable, Protocol, Any, cast
from typing_extensions import Self

from dataframe_api._types import SupportsDataFrameAPI

expensive_feature_engineering: Callable[[DataFrame], DataFrame]

class Model(Protocol):
    def __init__(self) -> None:
        ...
    def __call__(self) -> Self:
        ...
    def fit(self, x_train: Any, y_train: Any) -> Self:
        ...
    def predict(self, x_test: Any) -> Self:
        ...

MyFancyModel: Model

def split_train_and_predict(df_non_standard: SupportsDataFrameAPI) -> DataFrame:
    df = df_non_standard.__dataframe_consortium_standard__()
    namespace = df.__dataframe_namespace__()
    col = namespace.col

    df = expensive_feature_engineering(df)

    df_permissive = df.collect()
    train = df_permissive.filter(col("id") == 0)
    val = df_permissive.filter(col("id") == 1)

    x_train = train.drop_columns("y").to_array_object(namespace.Float64())
    y_train = train.get_column_by_name("y").to_array_object(namespace.Float64())
    x_val = val.drop_columns("y").to_array_object(namespace.Float64())
    y_val = val.get_column_by_name("y").to_array_object(namespace.Float64())
    xp = x_train.__array_namespace__()

    model = MyFancyModel()
    model.fit(x_train, y_train)
    preds = model.predict(x_val)

    results = xp.concat(
        [
            xp.expand_dims(preds, axis=1),
            xp.expand_dims(y_val, axis=1),
        ]
    )
    results_df: DataFrame = namespace.dataframe_from_2d_array(
        results,
        names=["preds", "true"],
        dtypes={"preds": namespace.Float64(), "true": namespace.Float64()},
    )
    return results_df
