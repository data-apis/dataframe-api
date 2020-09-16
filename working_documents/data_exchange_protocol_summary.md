# Dataframe exchange protocol - status summary

## Introduction

This document aims to summarize the recent discussions regarding the definition
of a data exchange protocol for dataframes.

Most of the discussion happened in [this GitHub issue](https://github.com/data-apis/dataframe-api/issues/29),
based on a proposal implementation by Wes McKinney in
[this pull request](https://github.com/wesm/dataframe-protocol/pull/1). And in
the [videocall of September 3rd, 2020](https://github.com/data-apis/workgroup/issues/10).

## Dataframe exchange protocol MVP

To simplify the problem, let's start by a very simple version of a dataframe
exchange protocol, based on [NumPy's array interface](https://numpy.org/doc/stable/reference/arrays.interface.html).

This version builds on top of the NumPy protocol, and is intended to be simple,
and not final, facilitating the discussion by changing or extending it. It only
supports simple types (integer, float).

In the example, we create a class `StandardDataFrame` that will be the producer of the data in the exchange. And we
create an instance of a two column dataframe, that will be shared with the protocol. The consumer will be pandas,
which is assumed to implement a `pandas.from_frame()` function, that can parse the data from the exchange protocol
and build a pandas dataframe.

```python
import array
import numpy


class ColumnInt:
    data = array.array('i', [1, 2, 3, 4])

    @property
    def name(self):
        return 'int_column'

    def to_numpy(self):
        return numpy(data)


class ColumnFloat:
    data = array.array('d', [1., 2., 3., 4.])

    @property
    def name(self):
        return 'float_column'

    def to_numpy(self):
        return numpy(data)


class StandardDataFrame:
    def __dataframe__(self):
        return {
            'len': 4,
            'columns': [ColInt(), ColFloat()]
            'version': 1,
        }

standard_df = StandardDataFrame()

pandas_df = pandas.from_dataframe(standard_df)
```

There are many limitations in this version, that will be discussed in the next sections:

- Requirement to import numpy in the consumer, even if it's not needed more than to export data
- Suboptimal performance of using Python structures. NumPy's array interface has a C implementation
  equivalent to the Python one `__array_struct__`, complementing `__array_interface__`. This can
  be done for dataframes too, but for simplicity only Python will be used in this document.
- No information on whether the data can be used directly (zero-copy) or if it needs to be copied
  by the producer
- No device support (e.g. sharing GPU memory, instead of CPU)
- Lack of support for complex times, such as strings, categorical, or types with missing values.
- Lack of support for columns not in memory (calculated/unmaterialized, in disk, in memory of workers
  not in the local host, etc)
- Implicit memory lifetime by not giving ownership

## Using a protocol instead of a container

In the first example, the exchange of the data was performed with a NumPy array. The consumer does
not necessarily need NumPy, since the data can be read using the array interface that the NumPy
array implements. But the producer needs to depend on NumPy, which may not be desired depending
on the dataframe implementation.

The immediate solution could be to simply replace the `.to_numpy()` function in the columns, by
the `__array_interface__` protocol. In the consumer, assuming the data wants to be received as a
NumPy array, the change is trivial:

```python
import numpy

def from_dataframe(df):
    first_column = df.__dataframe__()['columns'][0]

    # With the `to_numpy()` implementation:
    data_as_numpy = first_column.to_numpy()

    # With the array interface protocol
    data_as_numpy = numpy.array(first_column)
```

The producer, could still use NumPy for convenience if desired, since NumPy implements the array
interface, but it would be simple if it is preferred to not depend on it. For example, with the next code:

```python
import array


class ColumnInt:
    data = array.array('i', [1, 2, 3, 4])
    read_only = True

    @property
    def name(self):
        return 'int_column'

    def __array_interface__(self):
        pointer_to_data, length = self.data.buffer_info()
        return {
            'shape': (length,),
            'typestr': '|i16',
            'data': (pointer_to_data, self.read_only),
            'version': 3,
        }

[...]
```

## Complex columns

The array interface supports basic types (e.g. integer, float, boolean), but not
some other types common in dataframes, like strings, categories or integers with
missing values.

There are two main options to support complex types:

- Use another protocol that supports them, like Arrow, instead of the array interface
- Exchange the underlying simple types separately

### Apache Arrow

In the case of a categorical column, the data is usually stored as an array with the indices,
and an array with the categories. For example, if we want to store `['a', 'b', 'b', 'a']`,
we would have an array `[0, 1, 1, 0]`, and then the categories `['a', 'b']`, which would be
equivalent to `{0: 'a', 1: 'b'}`, the mapping of the indices to the actual values.

Similar to the array interface, Arrow implements an `__arrow_array__` that can support
the complex types defined by Arrow (like categories). An example using it could look like
the next code:

```python
import array
import pyarrow


class ColumnCategory:  # NOTE: That this is now a category
    indices = array.array('i', [0, 1, 1, 0])
    categories = array.array('u', ['a', 'b'])
    read_only = True

    @property
    def name(self):
        return 'category_column'

    def __arrow_array__(self):  # NOTE: This is now Arrow array protocol
        return pyarrow.DictionaryArray.from_arrays(self.indices,
                                                   self.categories)

[...]
```

Currently, the `__arrow_array__` protocol does not implement a protocol, but
it's just a way to exchange Arrow arrays. So, Arrow should be imported in the
producer, and the consumer will receive the data in an Arrow structure without
having to read it manually from the memory. This could be the implementation
of the consumer:

```python
import pyarrow

def from_dataframe(df):
    first_column = df.__dataframe__()['columns'][0]

    # Data is already an Arrow array, this is how `__arrow_array__` works.
    data_as_arrow = first_column
```

Arrow does provide the [Arrow C data interface](https://github.com/apache/arrow/blob/master/docs/source/format/CDataInterface.rst),
which is similar to NumPy's C array interface, implemented as `__array_struct__`. It does
not look like Arrow defines any dunder method (e.g. `__arrow_struct__`) that a C implementation
can be loaded to pyarrow with `pyarrow.array(obj)`, but that can probably be implemented quite
easily in Arrow or in a third party library.

Using Arrow can help with most types common in dataframes, but there are limitations (that can
or cannot be a problem, depending on the implementation):

- Lack of Python object support (e.g. strings as Python objects in pandas)
- Booleans represented in a single bit, and some implementations may prefer a one byte representation
- No support for bfloat type (not sure if any dataframe implementation uses them currently)
- Limited number of units for timestamps and durations (nano/micro/milli-seconds, and seconds are
  currently supported, see the full list in the [data format strings](https://arrow.apache.org/docs/format/CDataInterface.html#data-type-description-format-strings)
  section of the Arrow C data interface
- No support to specify the device, if the shared memory is not CPU memory (for example the data is
  in one of multiple GPUs)

### Sharing the underlying columns

In the previous section, Arrow is exchanging the categorical column as a whole.
Another alternative, is exchanging the components of the categorical column directly.

This will be somehow reinventing the wheel compared to Arrow, since we'll have to include
in the dataframe exchange protocol the representation of all the complex types. For example,
defining that a string is implemented as two arrays, one for the sequence of all strings,
and another for the offsets, etc.

The next example shows a possible implementation of exchanging the data by sharing the
underlying columns, with a dataframe of two columns, a categorical, and an integer columns.

Note that since the types are not simple, and shared directly in the arrays, or in the
Arrow structure, the dataframe exchange protocol needs to define an extra property to
specify the type (`dtype` in the example).

```python
import array


class ArrayContainer:
    def __init__(self, data, dtype, read_only):
        self.data = data
        self.dtype = dtype
        self.ready_only = read_only

    def __array_interface__(self):
        pointer_to_data, length = self.data.buffer_info()
        return {
            'shape': (length,),
            'typestr': self.dtype,
            'data': (pointer_to_data, self.read_only),
            'version': 3,
        }

class ColumnCategory:
    indices = array.array('i', [0, 1, 1, 0])
    categories = array.array('u', ['a', 'b'])
    read_only = True

    @property
    def name(self):
        return 'category_column'

    @property
    def dtype(self):
        return 'category'

    def data(self):
        return {
            'indices': ArrayContainer(data=self.indices,
                                      dtype='|i16',
                                      read_only=self.read_only),
            'categories': ArrayContainer(data=self.categories,
                                         dtype='|U8'),
        }

class ColumnInt:
    data = array.array('i', [1, 2, 3, 4])
    read_only = True

    @property
    def name(self):
        return 'int_column'

    @property
    def dtype(self):
        return 'int16'

    def data(self):
        return ArrayContainer(data=self.data,
                              dtype='|i16',
                              read_only=self.read_only)

[...]
```

## Supporting sources other than CPU memory (aka host memory or RAM)

The previous examples are using a buffer interface that shares the information
to access a region of CPU memory. While this can be the most obvious location of
the data, the data can actually be in different locations. Mainly:

- CPU memory (host memory)
- Memory of other devices (GPU, TPU, XPU, etc.)
- Disk (HDF5, Parquet, etc)
- Any of the two previous points, but distributed accross different machines
- The data is calculated (for example the sum of two other columns) and is not materialized

The simplest option from the dataframe exchange protocol point of view would be if
the producer materializes the data into CPI memory, and then the approaches of the previous
examples can simply be used. But this has some problems:

- The consumer may want the data in the same location where the producer has it
  (e.g. GPU memory or a Parquet file), and then two unnecessary copies of the
  memory would be required (to CPU memory, and back to the previous format)
- The data may be too big to be copied to CPU memory (the protocol can support batches to
  fix this problem)
- For calculated data, if the consumer also supports calculated data, copying the data
  to memory is not only inefficient, but the consumer wouldn't know that the data
  is calculated, and will be a regular column in the target dataframe

### Use cases

While supporting the exchange of most not in memory data can be out of the scope of this API,
let's explore few uses cases where using only memory will be limiting.

#### Machine learning of a GPU dataframe

We can think of a GPU-based dataframe implementation (e.g. cuDF), and a consumer that is able
to perform machine learning with dataframes in GPU data (e.g. cuML). Using a protocol based on
CPU memory only would mean that there would be two copies, `GPU -> CPU` in the producer and
`CPU -> GPU` in the consumer, which is very inefficient.

Sharing GPU memory adds a bit of complexity to the API, but since it's memory the main change
is supporting a device parameter, to specify in which device if the memory is located.

#### Out of memory plotting library

An out of memory dataframe like Vaex can have a dataframe where the data is not in memory, but
in disk, and it's only loaded in chunks when operations are performed. Libraries like datashader
can plot bigger than memory plots, by using a map/reduce-like approach, and could possibly
support disk data as a parameter.

For example, a very simple exchange interface for hdf5 files could be:

```python
class ColumnInt:
    file_name = '/var/data/my_dataframe.hdf5'
    table_name = 'my_table'
    column_name = 'int_column'
    read_only = True

    @property
    def name(self):
        return self.column_name

    def __hdf5_interface__(self):
        return {
            'typestr': 'int16',
            'file_name': self.file_name,
            'table_name': self.table_name,
            'column_name': self.column_name,
            'version': 1,
        }

[...]
```

This would be very similar to exchanging a pointer to memory, but since the data is not in
memory, the information to locate it in disk would be exchanged (the path in the filesystem,
and the information on how to locate the data in the file, like the column name).

Implementing interfaces like that for a limited set of known formats would not be difficult.
The main problem is that what needs to be shared is not the underlying data (the hdf5), but
the dataframe representation of it, applying all the (lazy) transformations that the user
performed. For example, if the user reads and hdf5 file in Vaex, applies a filter, adds a
calculated column that is the product of two columns in the hdf5 file, the consumer should
receive the information about these operations too, since this is what the user is aiming
to plot, not the original hdf5 file.

#### Exchanging information in Spark based dataframes

There are currently two main dataframe implementations based on Spark, PySpark and Koalas.
If we want to exchange data between Koalas and PySpark, the obvious thing to do would be
to share the underlying Spark data, and not serialize it in a single machine RAM, which
would likely be a very expensive operation. In this particular case, Koalas is built on top
of PySpark, so exchanging data may be trivial and not requiring a protocol, since both have
the same internal representation. But for independent Spark libraries, a memory exchange
protocol would be suboptimal.

#### Exchanging calculated columns from Ibis to Vaex

One last use case could be exchanging calculated columns. Ibis is a Python library that
allows creating SQL expressions with a pandas-like interface. The underlying data of
Ibis is a database (or also big data systems supporting SQL-like syntax, like Impala).

We can have the case, where a user created an Ibis expression `table.my_column + 1`, and
wants to convert its dataframe-like expression to Vaex (which supports calculated columns).
In this case, since the data is likely to be moved from a database (e.g. PostgreSQL) to
another representation supported by Vaex (Arrow, or a HDF5 file), most of the data will
have to be serialized. But ideally, the calculated column `table.my_column + 1` wouldn't
be serialized, since Vaex could receive it as a calculated column. This won't only make
the conversion (transfer of the data) faster, but would also reduce the size of the
final dataframe in Vaex.

To exchange a calculated column, probably the most reasonable way would be to exchange
a string with a formula (e.g. `my_column + 1`), which could refer to other columns in
the dataframe. SQL would probably be the obvious choice for representing formulas, but
SQL is only partially a standard, and it supports different variants (dialects), so for
complex expressions a particular dialect would need to be selected.

### Protocol scalability

From the previous use cases, seems reasonable to think that the protocol would benefit
of exchange of non-memory representations.

For the case of CPU memory and other memories (GPU, TPU, etc.) a single interface that
generalizes boths seem very feasible. But also, two interfaces could exist. For example
Arrow or NumPy's array interface for CPU memory, and a CUDA interface for GPU memory.
If we assume that the protocol can be extended in the future to support other interfaces
like the ones described above, it may be a good idea to implement the protocol in a way
that supports multiple interfaces, even if initially just CPU, or CPU and GPU interfaces
are used.

There are multiple ways to implement this, for example, dataframes could implement a
property to indicate the interface of the native location, and possibly support both, 
the native interface, and the memory interface.

```python
class ColumnCalculated:
    read_only = True

    @property
    def name(self):
        return 'int_column'

    @property
    def native_interface(self):
        return '__sql_interface__'

    def __sql_interface__(self):
        return 'original_column + 1'

    def __array_interface__(self):
        data = materialize(self.columns['original_column'] + 1)
        pointer_to_data, length = data.buffer_info()
        return {
            'shape': (length,),
            'typestr': '|i16',
            'data': (pointer_to_data, self.read_only),
            'version': 3,
        }

[...]
```

### Behavior when exchanging data in different formats

If there are more than one location supported by the protocol (even if it's just
CPU and GPU memories), a decision needs to be made on what happens when the
consumer expects data in a different location that the one the producer has.
For example, we have a cuDF dataframe that is stored in GPU memory. And
the user wants to convert it to pandas (e.g. `pandas.from_dataframe(cudf_df)`).
But pandas will store the data in CPU memory, and does not implement how to access
GPU memory. There are different options for the dataframe exchange protocol:

- Producers will simply expose the data they have, and consumers need to deal with
  converting it if needed, throwing an exception if it's a format they don't support
- Producers are able to fallback to CPU memory if the consumer doesn't support their
  native location
- Consumers can request the data with a list of supported formats, sorted by their
  preference, and producers will offer the one with highest priority they can
  support, or raise an exception, if none is supported
- Other ideas welcome

## Summary

To summarize the previous sections, this is a non-exhaustive list of the initial topics
that need to be decided (feel free to propose topics that are missing):

- What is the scope of the protocol regarding supported formats? CPU memory is the most
  obvious, GPU memory was discussed, but should it be in the first version of the protocol?
  Should the protocol support adding more formats in the future, like calculated columns?

- Should CPU memory and GPU memory use a single interface? Or they should be different?

- For CPU memory, do we want to use Arrow, or do we want to build our own protocol on top
  of the array interface, DLPack or something else?

- What is the expected behavior when the consumer and producer use different formats?
  Should an exception be thrown? Should producers be able to materialize data to CPU
  memory and offer it to consumers?
