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
   dataframe_from_columns
   dataframe_from_2d_array

The ``DataFrame``, ``Column`` and ``GroupBy`` objects have the following
methods and attributes:

.. toctree::
   :maxdepth: 3

   dataframe_object
   column_object
   groupby_object
