# Execution model

## Scope

The vast majority of the Dataframe API is designed to be agnostic of the
underlying execution model.

However, there are some methods which, depending on the implementation, may
not be supported in some cases.

For example, let's consider the following:
```python
df: DataFrame
features = []
for column_name in df.column_names:
    if df.col(column_name).std() > 0:
        features.append(column_name)
return features
```
If `df` is a lazy dataframe, then the call `df.col(column_name).std() > 0` returns
a (ducktyped) Python boolean scalar. No issues so far. Problem is,
what happens when `if df.col(column_name).std() > 0` is called?

Under the hood, Python will call `(df.col(column_name).std() > 0).__bool__()` in
order to extract a Python boolean. This is a problem for "lazy" implementations,
as the laziness needs breaking in order to evaluate the above.

Dask and Polars both require that `.compute` (resp. `.collect`) be called beforehand
for such an operation to be executed:
  ```python
  In [1]: import dask.dataframe as dd
  
  In [2]: pandas_df = pd.DataFrame({"x": [1, 2, 3], "y": 1})
  
  In [3]: df = dd.from_pandas(pandas_df, npartitions=2)
  
  In [4]: scalar = df.x.std() > 0
  
  In [5]: if scalar:
     ...:     print('scalar is positive')
     ...:
  ---------------------------------------------------------------------------
  [...]
  
  TypeError: Trying to convert dd.Scalar<gt-bbc3..., dtype=bool> to a boolean value. Because Dask objects are lazily evaluated, they cannot be converted to a boolean value or used in boolean conditions like if statements. Try calling .compute() to force computation prior to converting to a boolean value or using in a conditional statement.
  ```

## Solution: DataFrame.persist

The Dataframe API has a `DataFrame.persist` for addressing the above. We can use it to rewrite the code above
as follows:
```python
df: DataFrame
df = df.persist()
features = []
for column_name in df.column_names:
    if df.col(column_name).std() > 0:
        features.append(column_name)
return features
```

Note that `persist` is to be interpreted as a hint, rather than as a directive -
the implementation itself may decide
whether to force execution at this step, cache results, defer it to later and cache
results when they reach the current node, or ignore it.

Operations which require `DataFrame.persist` to have been called at some prior
point are:
- `DataFrame.shape`
- calling `bool`, `int`, or `float` on a scalar 

Note how in the above example, `DataFrame.persist` was called only once,
and as late as possible.
Conversely, the "wrong" way to execute the above would be:

```python
df: DataFrame
features = []
for column_name in df.column_names:
    # Do NOT do this!
    if df.persist().col(column_name).std() > 0:
        features.append(column_name)
return features
```
as that will potentially re-trigger the same execution multiple times.
