.. _dataframe-object:

Dataframe object
================

A conforming implementation of the dataframe API standard must provide and
support a dataframe object having the following attributes and methods.

-------------------------------------------------

.. _operators:

Operators
---------

A conforming implementation of the dataframe API standard must provide and
support a dataframe object supporting the following Python operators.

Arithmetic Operators
~~~~~~~~~~~~~~~~~~~~

A conforming implementation of the array API standard must provide and support
an array object supporting the following Python arithmetic operators.

-   `x1 + x2`: :meth:`.DataFrame.__add__`

    -   `operator.add(x1, x2) <https://docs.python.org/3/library/operator.html#operator.add>`_
    -   `operator.__add__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__add__>`_

-   `x1 - x2`: :meth:`.DataFrame.__sub__`

    -   `operator.sub(x1, x2) <https://docs.python.org/3/library/operator.html#operator.sub>`_
    -   `operator.__sub__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__sub__>`_

-   `x1 * x2`: :meth:`.DataFrame.__mul__`

    -   `operator.mul(x1, x2) <https://docs.python.org/3/library/operator.html#operator.mul>`_
    -   `operator.__mul__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__mul__>`_

-   `x1 / x2`: :meth:`.DataFrame.__truediv__`

    -   `operator.truediv(x1,x2) <https://docs.python.org/3/library/operator.html#operator.truediv>`_
    -   `operator.__truediv__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__truediv__>`_

-   `x1 // x2`: :meth:`.DataFrame.__floordiv__`

    -   `operator.floordiv(x1, x2) <https://docs.python.org/3/library/operator.html#operator.floordiv>`_
    -   `operator.__floordiv__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__floordiv__>`_

-   `x1 % x2`: :meth:`.DataFrame.__mod__`

    -   `operator.mod(x1, x2) <https://docs.python.org/3/library/operator.html#operator.mod>`_
    -   `operator.__mod__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__mod__>`_

-   `x1 ** x2`: :meth:`.DataFrame.__pow__`

    -   `operator.pow(x1, x2) <https://docs.python.org/3/library/operator.html#operator.pow>`_
    -   `operator.__pow__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__pow__>`_

Arithmetic operators should be defined for a dataframe having real-valued data types.


Comparison Operators
~~~~~~~~~~~~~~~~~~~~

A conforming implementation of the dataframe API standard must provide and
support a dataframe object supporting the following Python comparison
operators.

-   `x1 < x2`: :meth:`.DataFrame.__lt__`

    -   `operator.lt(x1, x2) <https://docs.python.org/3/library/operator.html#operator.lt>`_
    -   `operator.__lt__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__lt__>`_

-   `x1 <= x2`: :meth:`.DataFrame.__le__`

    -   `operator.le(x1, x2) <https://docs.python.org/3/library/operator.html#operator.le>`_
    -   `operator.__le__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__le__>`_

-   `x1 > x2`: :meth:`.DataFrame.__gt__`

    -   `operator.gt(x1, x2) <https://docs.python.org/3/library/operator.html#operator.gt>`_
    -   `operator.__gt__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__gt__>`_

-   `x1 >= x2`: :meth:`.DataFrame.__ge__`

    -   `operator.ge(x1, x2) <https://docs.python.org/3/library/operator.html#operator.ge>`_
    -   `operator.__ge__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__ge__>`_

-   `x1 == x2`: :meth:`.DataFrame.__eq__`

    -   `operator.eq(x1, x2) <https://docs.python.org/3/library/operator.html#operator.eq>`_
    -   `operator.__eq__(x1, x2) <https://docs.python.org/3/library/operator.html#operator.__eq__>`_

-   `x1 != x2`: :meth:`.DataFrame.__ne__`

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

TODO

..
  NOTE: please keep the attributes in alphabetical order


..
 autosummary::
   :toctree: generated
   :template: property.rst

   DataFrame.shape

-------------------------------------------------

Methods
-------
..
  NOTE: please keep the methods in alphabetical order


.. autosummary::
   :toctree: generated
   :template: property.rst

   DataFrame.__add__
   DataFrame.__eq__
   DataFrame.__floordiv__
   DataFrame.__ge__
   DataFrame.__gt__
   DataFrame.__le__
   DataFrame.__lt__
   DataFrame.__ne__
   DataFrame.__mod__
   DataFrame.__mul__
   DataFrame.__pow__
   DataFrame.__sub__
   DataFrame.__truediv__
