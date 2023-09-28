from typing import Any

from dataframe_api._types import SupportsDataFrameAPI

def my_dataframe_agnostic_function(df_non_standard: SupportsDataFrameAPI) -> Any:
    df = df_non_standard.__dataframe_consortium_standard__(api_version='2023.09-beta')

    for column_name in df.column_names:
        if column_name == 'species':
            continue
        new_column = df.get_column_by_name(column_name)
        new_column = (new_column - new_column.mean()) / new_column.std()
        df = df.assign(new_column.rename(f'{column_name}_scaled'))

    return df.dataframe
