# Execution model

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
  TypeError                                 Traceback (most recent call last)
  Cell In[5], line 1
  ----> 1 if scalar:
        2     print('scalar is positive')
  
  File ~/tmp/.venv/lib/python3.10/site-packages/dask/dataframe/core.py:312, in Scalar.__bool__(self)
      311 def __bool__(self):
  --> 312     raise TypeError(
      313         f"Trying to convert {self} to a boolean value. Because Dask objects are "
      314         "lazily evaluated, they cannot be converted to a boolean value or used "
      315         "in boolean conditions like if statements. Try calling .compute() to "
      316         "force computation prior to converting to a boolean value or using in "
      317         "a conditional statement."
      318     )
  
  TypeError: Trying to convert dd.Scalar<gt-bbc3..., dtype=bool> to a boolean value. Because Dask objects are lazily evaluated, they cannot be converted to a boolean value or used in boolean conditions like if statements. Try calling .compute() to force computation prior to converting to a boolean value or using in a conditional statement.
  ```

Exactly which methods require computation may vary across implementations. Some may
implicitly do it for users under-the-hood for certain methods, whereas others require
the user to explicitly trigger it.

Therefore, the Dataframe API has a `Dataframe.maybe_evaluate` method. This is to be
interpreted as a hint, rather than as a directive - the implementation itself may decide
whether to force execution at this step, or whether to defer it to later.

Operations which require `DataFrame.may_execute` to have been called at some prior
point are:
- `DataFrame.to_array`
- `DataFrame.shape`
- `Column.to_array`
- calling `bool`, `int`, or `float` on a scalar 

Therefore, the Standard-compliant way to write the code above is:
```python
df: DataFrame
df = df.may_execute()
features = []
for column_name in df.column_names:
    if df.col(column_name).std() > 0:
        features.append(column_name)
return features
```

Note now `DataFrame.may_execute` is called only once, and as late as possible.
Conversely, the "wrong" way to execute the above would be:

```python
df: DataFrame
features = []
for column_name in df.column_names:
    # Do NOT do this!
    if df.may_execute().col(column_name).std() > 0:
        features.append(column_name)
return features
```
as that will potentially re-trigger the same execution multiple times.
