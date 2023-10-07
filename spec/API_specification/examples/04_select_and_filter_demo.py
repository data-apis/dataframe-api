from dataframe_api import DataFrame

df: DataFrame
namespace = df.__dataframe_namespace__()
col = namespace.col

# You can select columns using column names or columns
# the following are all valid
df.select("a")
df.select("a", "b")
df.select(col("a"))
df.select((col("a") + 1).rename("b"))

# You can filter using columns
df = df.filter(col("width") > col("height"))

# PermissiveColumn can be thought of as a trivial column.
# So, filtering using PermissiveColumn works too, though is more verbose
df_permissive = df.collect()
df_permissive = df_permissive.filter(
    df_permissive.get_column_by_name("width")
    > df_permissive.get_column_by_name("height")
)
