.. _api-specification:

API specification
=================

.. currentmodule:: dataframe_api

The API consists of dataframe, column and groupby classes, plus a small number
of objects and functions in the top-level namespace. The latter are:

.. autosummary::
   :toctree: generated
   :template: attribute.rst
   :nosignatures:

   __dataframe_api_version__
   is_null
   null
   col
   sorted_indices
   unique_indices
   any_rowwise
   all_rowwise
   Int64
   Int32
   Int16
   Int8
   UInt64
   UInt32
   UInt16
   UInt8
   Float64
   Float32
   Bool
   Date
   Datetime
   Duration
   String
   is_dtype
   column_from_sequence
   column_from_1d_array
   dataframe_from_dict
   dataframe_from_2d_array

The ``DataFrame``, ``PermissiveFrame``, ``PermissiveColumn``, ``Column`` and ``GroupBy`` objects have the following
methods and attributes:

.. toctree::
   :maxdepth: 3

   dataframe_object
   permissiveframe_object
   permissivecolumn_object
   column_object
   groupby_object
