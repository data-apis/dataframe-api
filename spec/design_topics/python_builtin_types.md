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
    def get_column(self, name: str, /) -> Column:
        ...

class Column:
    def mean(self, skip_nulls: bool = True) -> float | NullType:
        ...

larger = df2 > df1.get_column('foo').mean()
```

For a GPU dataframe library, it is desirable for all data to reside on the GPU,
and not incur a performance penalty from synchronizing instances of Python
builtin types to CPU. In the above example, the `.mean()` call returns a
`float`. It is likely beneficial though to implement this as a library-specific
scalar object which duck types with `float`. This means that it should (a) have
the same semantics as a builtin `float` when used within a library, and (b)
support usage as a `float` outside of the library (i.e., implement
`__float__`). Duck typing is usually not perfect, for example `isinstance`
usage on the float-like duck type will behave differently. Such explicit "type
of object" checks don't have to be supported.

The following design rule applies everywhere builtin Python types are used
within this API standard: _where a Python builtin type is specified, an
implementation may always replace it by an equivalent library-specific type
that duck types with the Python builtin type._
