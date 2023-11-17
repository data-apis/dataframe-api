# Python builtin types and duck typing

Use of Python's builtin types - `bool`, `int`, `float`, `str`, `dict`, `list`,
`tuple`, `datetime.datetime`, etc. - is often natural and convenient. However,
it is also potentially problematic when trying to write performant dataframe
library code or supporting devices other than CPU.

This standard specifies the use of Python types in quite a few places, and uses
them as type annotations. As a concrete example, consider the `mean` method,
the `bool | Scalar` argument it takes, and the `Scalar` it is documented to return,
in combination with the `__gt__` method (i.e., the `>` operator) on the dataframe:

```python
class DataFrame:
    def __gt__(self, other: DataFrame | Scalar) -> DataFrame:
        ...
    def col(self, name: str, /) -> Column:
        ...

class Column:
    def mean(self, skip_nulls: bool | Scalar = True) -> Scalar:
        ...

larger = df2 > df1.col('foo', skip_nulls = True).mean()
```

Let's go through these arguments:
- `skip_nulls: bool | Scalar`. This means we can either pass a Python `bool`, or
  a `Scalar` object backed by a boolean;
- the return value of `.mean()` is a `Scalar`
- the argument `other` of `__gt__` is typed as `AnyScalar`, meaning that we can
  compare a `DataFrame` with a Python scalar (e.g. `df > 3`) or with a `Scalar`
  (e.g. `df > df.col('a').mean()`)
- the return value of `__gt__` is a `Scalar`

Returning values as `Scalar` allows scalars to reside on different devices (e.g. GPU),
or to stay lazy (if a library allows it).

## Example

For example, if a library implements `FancyFloat` and `FancyBool` scalars,
then the following should all be supported:
```python
df: DataFrame
column_1: Column = df.col('a')
column_2: Column = df.col('b')

scalar: FancyFloat = column_1.std()
result_1: Column = column_2 - column_1.std()
result_2: FancyBool = column_2.std() > column_1.std()
```

Note that the scalars above are library-specific ones - they may be used to keep
data on GPU, or to keep data lazy.

The following, however, may raise, dependening on the
implementation:
```python
df: DataFrame
column = df.col('a')

if column.std() > 0:  # this line may raise!
    print('std is positive')
```
This is because `if column.std() > 0` will call `(column.std() > 0).__bool__()`,
which is required by Python to produce a Python scalar.
Therefore, a purely lazy dataframe library may choose to raise here, whereas as
one which allows for eager execution may return a Python bool.
