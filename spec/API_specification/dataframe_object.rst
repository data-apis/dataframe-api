.. _array-object:

Dataframe object
================

A conforming implementation of the dataframe API standard must provide and
support an array object having the following attributes and methods.

-------------------------------------------------

.. _operators:

Operators
---------

A conforming implementation of the array API standard must provide and support an array object supporting the following Python operators.

Arithmetic Operators
~~~~~~~~~~~~~~~~~~~~

A conforming implementation of the array API standard must provide and support an array object supporting the following Python arithmetic operators.

-   ``+x``: :meth:`.dataframe.__pos__`

    -   `operator.pos(x) <https://docs.python.org/3/library/operator.html#operator.pos>`_
    -   `operator.__pos__(x) <https://docs.python.org/3/library/operator.html#operator.__pos__>`_

-   `-x`: :meth:`.dataframe.__neg__`

    -   `operator.neg(x) <https://docs.python.org/3/library/operator.html#operator.neg>`_
    -   `operator.__neg__(x) <https://docs.python.org/3/library/operator.html#operator.__neg__>`_

-   `x1 + x2`: :meth:`.dataframe.__add__`

    -   `operator.add(x1, x2) <https://docs.python.org/3/library/operator.html#operator.add>`_
    -   `operator.__add__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__add__>`_

-   `x1 - x2`: :meth:`.dataframe.__sub__`

    -   `operator.sub(x1, x2) <https://docs.python.org/3/library/operator.html#operator.sub>`_
    -   `operator.__sub__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__sub__>`_

-   `x1 * x2`: :meth:`.dataframe.__mul__`

    -   `operator.mul(x1, x2) <https://docs.python.org/3/library/operator.html#operator.mul>`_
    -   `operator.__mul__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__mul__>`_

-   `x1 / x2`: :meth:`.dataframe.__truediv__`

    -   `operator.truediv(x1,x2) <https://docs.python.org/3/library/operator.html#operator.truediv>`_
    -   `operator.__truediv__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__truediv__>`_

-   `x1 // x2`: :meth:`.dataframe.__floordiv__`

    -   `operator.floordiv(x1, x2) <https://docs.python.org/3/library/operator.html#operator.floordiv>`_
    -   `operator.__floordiv__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__floordiv__>`_

-   `x1 % x2`: :meth:`.dataframe.__mod__`

    -   `operator.mod(x1, x2) <https://docs.python.org/3/library/operator.html#operator.mod>`_
    -   `operator.__mod__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__mod__>`_

-   `x1 ** x2`: :meth:`.dataframe.__pow__`

    -   `operator.pow(x1, x2) <https://docs.python.org/3/library/operator.html#operator.pow>`_
    -   `operator.__pow__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__pow__>`_

Arithmetic operators should be defined for dataframe having real-valued data types.

Array Operators
~~~~~~~~~~~~~~~

A conforming implementation of the array API standard must provide and support an array object supporting the following Python array operators.

-   `x1 @ x2`: :meth:`.dataframe.__matmul__`

    -   `operator.matmul(x1, x2) <https://docs.python.org/3/library/operator.html#operator.matmul>`_
    -   `operator.__matmul__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__matmul__>`_

The matmul ``@`` operator should be defined for arrays having real-valued data types.

Bitwise Operators
~~~~~~~~~~~~~~~~~

A conforming implementation of the array API standard must provide and support an array object supporting the following Python bitwise operators.

-   `~x`: :meth:`.dataframe.__invert__`

    -   `operator.inv(x) <https://docs.python.org/3/library/operator.html#operator.inv>`_
    -   `operator.invert(x) <https://docs.python.org/3/library/operator.html#operator.invert>`_
    -   `operator.__inv__(x) <https://docs.python.org/3/library/operator.html#operator.__inv__>`_
    -   `operator.__invert__(x) <https://docs.python.org/3/library/operator.html#operator.__invert__>`_

-   `x1 & x2`: :meth:`.dataframe.__and__`

    -   `operator.and(x1, x2) <https://docs.python.org/3/library/operator.html#operator.and>`_
    -   `operator.__and__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__and__>`_

-   `x1 | x2`: :meth:`.dataframe.__or__`

    -   `operator.or(x1, x2) <https://docs.python.org/3/library/operator.html#operator.or>`_
    -   `operator.__or__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__or__>`_

-   `x1 ^ x2`: :meth:`.dataframe.__xor__`

    -   `operator.xor(x1, x2) <https://docs.python.org/3/library/operator.html#operator.xor>`_
    -   `operator.__xor__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__xor__>`_

-   `x1 << x2`: :meth:`.dataframe.__lshift__`

    -   `operator.lshift(x1, x2) <https://docs.python.org/3/library/operator.html#operator.lshift>`_
    -   `operator.__lshift__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__lshift__>`_

-   `x1 >> x2`: :meth:`.dataframe.__rshift__`

    -   `operator.rshift(x1, x2) <https://docs.python.org/3/library/operator.html#operator.rshift>`_
    -   `operator.__rshift__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__rshift__>`_

Bitwise operators should be defined for arrays having integer and boolean data types.

Comparison Operators
~~~~~~~~~~~~~~~~~~~~

A conforming implementation of the dataframe API standard must provide and
support a dataframe object supporting the following Python comparison
operators.

-   `x1 < x2`: :meth:`.dataframe.__lt__`

    -   `operator.lt(x1, x2) <https://docs.python.org/3/library/operator.html#operator.lt>`_
    -   `operator.__lt__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__lt__>`_

-   `x1 <= x2`: :meth:`.dataframe.__le__`

    -   `operator.le(x1, x2) <https://docs.python.org/3/library/operator.html#operator.le>`_
    -   `operator.__le__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__le__>`_

-   `x1 > x2`: :meth:`.dataframe.__gt__`

    -   `operator.gt(x1, x2) <https://docs.python.org/3/library/operator.html#operator.gt>`_
    -   `operator.__gt__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__gt__>`_

-   `x1 >= x2`: :meth:`.dataframe.__ge__`

    -   `operator.ge(x1, x2) <https://docs.python.org/3/library/operator.html#operator.ge>`_
    -   `operator.__ge__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__ge__>`_

-   `x1 == x2`: :meth:`.dataframe.__eq__`

    -   `operator.eq(x1, x2) <https://docs.python.org/3/library/operator.html#operator.eq>`_
    -   `operator.__eq__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__eq__>`_

-   `x1 != x2`: :meth:`.dataframe.__ne__`

    -   `operator.ne(x1, x2) <https://docs.python.org/3/library/operator.html#operator.ne>`_
    -   `operator.__ne__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__ne__>`_

Comparison operators should be defined for dataframes having any data type.

In-place Operators
~~~~~~~~~~~~~~~~~~

TODO

Reflected Operators
~~~~~~~~~~~~~~~~~~~

TODO

Arithmetic Operators
""""""""""""""""""""

-   ``__radd__``
-   ``__rsub__``
-   ``__rmul__``
-   ``__rtruediv__``
-   ``__rfloordiv__``
-   ``__rpow__``
-   ``__rmod__``

-------------------------------------------------

.. currentmodule:: dataframe_api

Attributes
----------
..
  NOTE: please keep the attributes in alphabetical order


.. autosummary::
   :toctree: generated
   :template: property.rst

   dataframe.shape

-------------------------------------------------

Methods
-------
..
  NOTE: please keep the methods in alphabetical order


.. autosummary::
   :toctree: generated
   :template: property.rst

   dataframe.__abs__
   dataframe.__add__
   dataframe.__dataframe_namespace__
   dataframe.__complex__
   dataframe.__eq__
   dataframe.__float__
   dataframe.__floordiv__
   dataframe.__ge__
   dataframe.__getitem__
   dataframe.__gt__
   dataframe.__int__
   dataframe.__le__
   dataframe.__lt__
   dataframe.__mod__
   dataframe.__mul__
   dataframe.__ne__
   dataframe.__neg__
   dataframe.__or__
   dataframe.__pos__
   dataframe.__pow__
   dataframe.__setitem__
   dataframe.__sub__
   dataframe.__truediv__
