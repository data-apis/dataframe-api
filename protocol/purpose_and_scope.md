# Purpose and scope

```{note}

This document is ready for wider community feedback, but still contains a
number of TODOs, and is expected to change and evolve before a first official
release. At least two independent implementation are also needed, in order to
validate the design and find potential issues.
```

## Introduction

Python users today have a number of great choices for dataframe libraries.
From Pandas and cuDF to Vaex, Koalas, Modin, Ibis, and more. Combining multiple
types of dataframes in a larger application or analysis workflow, or developing
a library which uses dataframes as a data structure, presents a challenge
though. Those libraries all have different APIs, and there is no standard way
of converting one type of dataframe into another.


### This dataframe protocol

The purpose of this dataframe protocol (`__dataframe__`) is to enable _data
interchange_. I.e., a way to convert one type of dataframe into another type
(for example, convert a Koalas dataframe into a Pandas dataframe, or a cuDF
dataframe into a Vaex dataframe).

Currently (July 2021) there is no way to do this in an
implementation-independent way.

A main use case this protocol intends to enable is to make it possible to
write code that can accept any type of dataframe instead of being tied to a
single type of dataframe. To illustrate that:

```python
def somefunc(df, ...):
    """`df` can be any dataframe supporting the protocol, rather than (say)
    only a pandas.DataFrame"""
    # could also be `cudf.from_dataframe(df)`, or `vaex.from_dataframe(df)`
    # note: this should throw a TypeError if it cannot be done without a device
    # transfer (e.g. move data from GPU to CPU) - add `force=True` in that case
    new_pandas_df = pd.from_dataframe(df)
    # From now on, use Pandas dataframe internally
```

It is important to note that providing a _complete, standardized dataframe API_
is not a goal of the `__dataframe__` protocol. Instead, this is a goal of the
full dataframe API standard, which the Consortium for Python Data API Standards
aims to develop in the future. When that full API standard is implemented by
dataframe libraries, the example above can change to:

```python
def get_df_module(df):
    """Utility function to support programming against a dataframe API"""
    if hasattr(df, '__dataframe_namespace__'):
       # Retrieve the namespace
       pdx = df.__dataframe_namespace__()
    else:
        # Here we can raise an exception if we only want to support compliant dataframes,
        # or convert to our default choice of dataframe if we want to accept (e.g.) dicts
        pdx = pd
        df = pd.DataFrame(df)

    return pdx, df


def somefunc(df, ...):
    """`df` can be any dataframe conforming to the dataframe API standard"""
    pdx, df = get_df_module(df)
    # From now on, use `df` methods and `pdx` functions/objects
```


### History

Dataframe libraries in several programming language exist, such as
[R](https://www.rdocumentation.org/packages/base/versions/3.6.2/topics/data.frame),
[Scala](https://docs.databricks.com/spark/latest/dataframes-datasets/introduction-to-dataframes-scala.html),
[Julia](https://juliadata.github.io/DataFrames.jl/stable/) and others.

In Python, the most popular dataframe library is [pandas](https://pandas.pydata.org/).
pandas was initially developed at a hedge fund, with a focus on
[panel data](https://en.wikipedia.org/wiki/Panel_data) and financial time series.
It was open sourced in 2009, and since then it has been growing in popularity, including
many other domains outside time series and financial data. While still rich in time series
functionality, today is considered a general-purpose dataframe library. The original
`Panel` class that gave name to the library was deprecated in 2017 and removed in 2019,
to focus on the main `DataFrame` class.

Internally, pandas is implemented (mostly) on top of NumPy, which is used to
store the data and to perform many of the operations. Some parts of pandas are
written in Cython.

Other libraries emerged in the last years, to address some of the limitations of pandas.
But in most cases, the libraries implemented a public API very similar to pandas, to
make the transition to their libraries easier. The next section provides a
short description of the main dataframe libraries in Python.

#### Python dataframe libraries

[Dask](https://dask.org/) is a task scheduler built in Python, which implements a
dataframe interface. Dask dataframe uses pandas internally in the workers, and it provides
an API similar to pandas, adapted to its distributed and lazy nature.

[Vaex](https://vaex.io/) is an out-of-core alternative to pandas. Vaex uses hdf5 to
create memory maps that avoid loading data sets to memory. Some parts of Vaex are
implemented in C++.

[Modin](https://github.com/modin-project/modin) is a distributed dataframe
library originally built on [Ray](https://github.com/ray-project/ray), but has
a more modular way, that allows it to also use Dask as a scheduler, or replace the
pandas-like public API by a SQLite-like one.

[cuDF](https://github.com/rapidsai/cudf) is a GPU dataframe library built on top
of Apache Arrow and RAPIDS. It provides an API similar to pandas.

[PySpark](https://spark.apache.org/docs/latest/api/python/index.html) is a
dataframe library that uses Spark as a backend. PySpark public API is based on the
original Spark API, and not in pandas.

[Koalas](https://github.com/databricks/koalas) is a dataframe library built on
top of PySpark that provides a pandas-like API.

[Ibis](https://ibis-project.org/) is a dataframe library with multiple SQL backends.
It uses SQLAlchemy and a custom SQL compiler to translate its pandas-like API to
SQL statements, executed by the backends. It supports conventional DBMS, as well
as big data systems such as Apache Impala or BigQuery.

#### History of this dataframe protocol

While there is no dataframe protocol like the one described in this document in
Python yet, there is a long history of _array_ interchange protocols - the
Python buffer protocol, various NumPy protocols like `__array_interface__`,
DLPack, and more.

A number of people have discussed creating a similar protocol for dataframes.
Such discussions gained momentum when Gael Varoquaux discussed the possibility
of a dataframe interchange protocol last year in a
[Discourse thread](https://discuss.ossdata.org/t/a-dataframe-protocol-for-the-pydata-ecosystem/26).
In response, Wes McKinney implemented an initial
[prototype](https://github.com/wesm/dataframe-protocol/pull/1). The
conversation and prototype generated a number of good ideas and stimulating
discussions; however, the topic was complex enough to necessitate a more
comprehensive approach, including collecting requirements and use cases from
a large set of stakeholders. This protocol is a natural follow-up to those
early discussions, and is taking exactly such a comprehensive approach.


(Scope)=

## Scope (includes out-of-scope / non-goals)

This section outlines what is in scope and out of scope for this dataframe
interchange protocol.

### In scope

The scope of the dataframe interchange protocol includes:

- Functionality which needs to be included in a dataframe library for it to
  support this protocol.
- Names of the relevant methods and functions.
- Function signatures, including type annotations.
- Semantics of functions and methods.
- Data type and device support.
- Memory ownership and lifetime.
- Basic dataframe metadata.


### Out of scope

1. Providing a full dataframe API is out of scope.

   _Rationale: this is a much larger undertaking, ._

2. Non-Python API standardization (e.g., C/C++ APIs)

3. Standardization of these dtypes is out of scope: object dtype,
   nested/structured dtypes, and custom dtypes via an extension mechanism.

   _Rationale: object dtypes are inefficient and may contain anything (so hard
   to support in a sensible way); nested/structures dtypes may be supported in
   the future but are not used that much and are complex to implement; custom
   dtypes would increase design complexity that is not justified._

4. Strided data storage, i.e. data that is regularly laid out but not
   contiguous in memory, is out of scope.

   _Rationale: not all libraries support strided data (e.g., Apache Arrow).
   Adding support to avoid copies may not have many real-world benefits._

5. "virtual columns", i.e. columns for which the data is not yet in memory
   because it uses lazy evaluation, are not supported other than through
   letting the producer materialize the data in memory when the consumer
   calls `__dataframe__`.

   _Rationale: the full dataframe API will support this use case by
   "programming to an interface"; this data interchange protocol is
   fundamentally built around describing data in memory_.


**Non-goals** for the API standard include:

- Providing a full dataframe API to enable "programming to an API".

### Constraints

An important constraint on the `__dataframe__` protocol is that it should not
make achieving the goal of the complete standardized dataframe API more
difficult to achieve.

There is a small concern here. Say that a library adopts `__dataframe__` first,
and it goes from supporting only Pandas to officially supporting other
dataframes like `modin.pandas.DataFrame`. At that point, changing to
supporting the full dataframe API standard as a next step _implies a
backwards compatibility break_ for users that now start relying on Modin
dataframe support. E.g., the second transition will change from returning a
Pandas dataframe from `somefunc(df_modin)` to returning a Modin dataframe
later. It must be made very clear to libraries accepting `__dataframe__` that
this is a consequence, and that that should be acceptable to them.


### Progression / timeline

- **Current status**: most dataframe-consuming libraries work _only_ with
  Pandas, and rely on many Pandas-specific functions, methods and behavior.
- **Status after `__dataframe__`**: with minor code changes (as in first
  example above), libraries can start supporting all conforming dataframes,
  convert them to Pandas dataframes, and still rely on the same
  Pandas-specific functions, methods and behavior.
- **Status after standard dataframe API adoption**: libraries can start
  supporting all conforming dataframes _without converting to Pandas or
  relying on its implementation details_. At this point, it's possible to
  "program to an interface" rather than to a specific library like Pandas.


## Stakeholders

Dataframes are a key element of data science workflows and appplications. Hence
there are many stakeholders for a dataframe protocol like this.  The _direct_
stakeholders of this standard are authors/maintainers of
Python dataframe libraries. There are many more types of _indirect_ stakeholders
though, including:

- maintainers of libraries and other programs which depend on dataframe libraries
  (called "dataframe-consuming libraries" in the rest of this document)
- Python dataframe end users
- authors of non-Python dataframe libraries

Libraries that are being most actively considered during the creation of the
first version of this protocol include:

- [pandas](https://pandas.pydata.org)
- [Dask](https://dask.org/)
- [cuDF](https://github.com/rapidsai/cudf)
- [Vaex](https://vaex.io/)
- [Modin](https://github.com/modin-project/modin)
- [Koalas](https://github.com/databricks/koalas)
- [Ibis](https://ibis-project.org/)

Other Python dataframe libraries that are currently under active development and
could adopt this protocol include:

- [PySpark](https://spark.apache.org/docs/latest/api/python/)
- [Turi Create](https://github.com/apple/turicreate)

Other relevant projects that provide "infrastructure" for dataframe libraries
to build on, include:

- [Apache Arrow](https://arrow.apache.org/) and its Python bindings [PyArrow](https://arrow.apache.org/docs/python)
- [NumPy](https://numpy.org/)

There are a lot of dataframe-consuming libraries; some of the most
prominent ones include:

- [scikit-learn](https://scikit-learn.org/)
- [Matplotlib](https://matplotlib.org/)
- [Seaborn](https://seaborn.pydata.org/)
- [pyjanitor](https://pyjanitor.readthedocs.io/)

Compilers, runtimes, and dispatching layers for which this API standard may be
relevant:

- TODO


(how-to-adopt-this-protocol)=

## How to adopt this protocol

To adopt the protocol, a dataframe library must implement a method named
`__dataframe__` on its dataframe class/object.

_TODO: versioning the protocol_


