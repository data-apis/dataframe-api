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
    def mean(self, skip_nulls: bool = True) -> float | NullType:
        ...

larger = df2 > df1.col('foo').mean()
```

For a GPU dataframe library, it is desirable for all data to reside on the GPU,
and not incur a performance penalty from synchronizing instances of Python
builtin types to CPU. In the above example, the `.mean()` call returns a
`float`. It is likely beneficial though to implement this as a library-specific
scalar object which duck types with `float`. This means that it should (a) have
the same semantics as a builtin `float` when used within a library, and (b)
support usage as a `float` outside of the library (see below).
Duck typing is usually not perfect, for example `isinstance`
usage on the float-like duck type will behave differently. Such explicit "type
of object" checks don't have to be supported.

The following design rule applies everywhere builtin Python types are used
within this API standard: _where a Python builtin type is specified, an
implementation may always replace it by an equivalent library-specific type
that duck types with the Python builtin type._

## Required methods

If a library doesn't use the Python built-in scalars, then its scalars must implement
at least the following operations which return scalars:
- `__lt__`
- `__le__`
- `__eq__`
- `__ne__`
- `__gt__`
- `__ge__`
- `__add__`
- `__radd__`
- `__sub__`
- `__rsub__`
- `__mul__`
- `__rmul__`
- `__mod__`
- `__rmod__`
- `__pow__`
- `__rpow__`
- `__floordiv__`
- `__rfloordiv__`
- `__truediv__`
- `__rtruediv__`
- `__neg__`
- `__abs__`

Furthermore, unless the library exclusively allows for lazy execution,
it must also implement the following unary operations which return Python scalars:
- `__int__`
- `__float__`
- `__bool__`

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
The following, however, may raise, dependening on the
implementation:
```python
df: DataFrame
column = df.col('a')

if column.std() > 0:  # this line may raise!
    print('std is positive')
```
This is because `if column.std() > 0` will call `(column.std() > 0).__bool__()`,
which must produce a Python scalar. Therefore, a purely lazy dataframe library
may choose to raise here, whereas as one which allows for eager execution may return
a Python bool.
