# Execution model

## Scope

The vast majority of the Dataframe API is designed to be agnostic of the
underlying execution model.

However, there are some methods which, depending on the implementation, may
not be supported in some cases.

For example, let's consider the following:
```python
df: DataFrame
features = [col.name for col in df.columns_iter() if col.std() > 0]
```
If `df` is a lazy dataframe, then the call `col.std() > 0` returns
a (ducktyped) Python boolean scalar. No issues so far. Problem is,
what happens when `if col.std() > 0` is called?

Under the hood, Python will call `(col.std() > 0).__bool__()` in
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

Whether such computation succeeds or raises is currently not defined by the Standard and may vary across
implementations.
