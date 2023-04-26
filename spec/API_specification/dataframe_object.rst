.. _dataframe-object:

Dataframe object
================

A conforming implementation of the dataframe API standard must provide and
support a dataframe object having the following attributes and methods.

Operators
---------

A conforming implementation of the dataframe API standard must provide and
support a dataframe object supporting the following Python operators.

Arithmetic Operators
~~~~~~~~~~~~~~~~~~~~

A conforming implementation of the array API standard must provide and support
a dataframe object supporting the following Python arithmetic operators.

Arithmetic operators should be defined for a dataframe having real-valued data types.

.. note::

   TODO: figure out whether we want to add ``__neg__`` and ``__pos__``, those
   are the two missing arithmetic operators.


Comparison Operators
~~~~~~~~~~~~~~~~~~~~

A conforming implementation of the dataframe API standard must provide and
support a dataframe object supporting the following Python comparison
operators.

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

.. currentmodule:: dataframe_api

.. autoclass:: DataFrame
