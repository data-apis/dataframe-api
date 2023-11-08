# Python builtin types and duck typing

Use of Python's builtin types - `bool`, `int`, `float`, `str`, `dict`, `list`,
`tuple`, `datetime.datetime`, etc. - is often natural and convenient. However,
it is also potentially problematic when trying to write performant dataframe
library code or supporting devices other than CPU.

This standard specifies the use of Python types in quite a few places, and uses
them as type annotations. As a concrete example, consider the `mean` method and
the `float` it is documented to return, in combination with the `__gt__` method
(i.e., the `>` operator) on the dataframe:

```python
class DataFrame:
    def __gt__(self, other: DataFrame | Scalar) -> DataFrame:
        ...
    def col(self, name: str, /) -> Column:
        ...

class Column:
    def mean(self, skip_nulls: bool = True) -> Scalar | NullType:
        ...

larger = df2 > df1.col('foo').mean()
```

For a GPU dataframe library, it is desirable for all data to reside on the GPU,
and not incur a performance penalty from synchronizing instances of Python
builtin types to CPU. In the above example, the `.mean()` call returns a
`Scalar`. It is likely beneficial though to implement this as a library-specific
scalar object which (partially) duck types with `float`. The required methods it
must implement are listed in `:class:Scalar`.

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
