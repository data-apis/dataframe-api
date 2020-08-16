# Purpose and scope

## Introduction

This document defines a Python data frame API.

A data frame is a programming interface for expressing data manipulations over a
data structure consisting of rows and columns. Columns are named, and values in a
column share a common data type. This definition is intentionally left broad.


## History

In 2009 [pandas](https://pandas.pydata.org/) became the first major Python data frame
library to be open sourced. Its popularity has been growing, and as of 2020 the pandas
website has around one million and a half visitors per month.

pandas is rich in features, and its public API contains more than 2,000 objects. In
recent years, the number of existing Python data frame libraries has been growing. Most
of the new libraries offer some advantages compared to pandas (distributed, out-of-core
or GPU computing for example). And most of them provide a public API very similar to pandas,
to make the transition easy to users. The main libraries in this category would be
[Dask](https://dask.org/), [Vaex](https://vaex.io/), [Modin](https://github.com/modin-project/modin),
[cuDF](https://github.com/rapidsai/cudf) and [Koalas](https://github.com/databricks/koalas).

There are other libraries that did not base their public API in pandas, the most popular
one is [PySpark](https://spark.apache.org/docs/latest/api/python/index.html) which bases
its API in the Spark data frame.


## Goals

Given the growing Python data frame ecosystem, and its complexity, this document provides
a standard Python data frame API. Until recently, pandas has been a de-facto standard for
Python data frames. But currently there are a growing number of not only data frame libraries,
but also libraries that interact with data frames (visualization, statistical or machine learning
libraries for example). Interactions among libraries are becoming complex, and the pandas
public API is suboptimal as a standard, for its size, complexity, and implementation details
it exposes.

The goal of the API described in this document is to provide a standard interface that encapsulates
implementation details of data frame libraries. This will allow users and third-party libraries to
write code that interacts with a standard data frame, and not with specific implementations.

The defined API does not aim to be a convenient API for all users of data frames. Libraries targeting
specific users (data analysts, data scientists, quants, etc.) can be implemented on top of the
standard API. The standard API is targeted to software engineers, who will build code and libraries
using the API specification following proper software engineering techniques.

See the [use cases](02_use_cases.html) section for details on the exact use cases considered.

## Scope

It is in the scope of this document the different elements of the API:

- Data structures and Python classes
- Functions and methods
- Expected returns of the different operations
- Data types (Python and low-level types)

The scope of this document is limited to generic data frames, and not data frames specific to
certain domains.


### Out-of-scope and non-goals

Implementation details of the data frames and execution of operations. This includes:

- How data is represented and stored (whether the data is in memory, disk, distributed)
- Expectations on when the execution is happening (in an eager or lazy way)


## Stakeholders

This section provides the list of stakeholders considered for the definition of this API.


### Data frame library authors

Authors of data frame libraries in Python are expected to implement the API defined
in this document in their libraries.

The list of known Python data frame libraries at the time of writing this document is next:

- [pandas](https://pandas.pydata.org/)
- [Dask](https://dask.org/)
- [cuDF](https://github.com/rapidsai/cudf)
- [Modin](https://github.com/modin-project/modin)
- [Vaex](https://vaex.io/)
- [Turi Create](https://github.com/apple/turicreate)
- [Koalas](https://github.com/databricks/koalas)
- [PySpark](https://spark.apache.org/docs/latest/api/python/index.html)
- [Grizzly](https://github.com/weld-project/weld#grizzly)
- [Mars](https://docs.pymars.org/en/latest/)
- [StaticFrame](https://static-frame.readthedocs.io/en/latest/)
- [dexplo](https://github.com/dexplo/dexplo/)
- [datatable](https://github.com/h2oai/datatable)
- [Eland](https://github.com/elastic/eland)


### Downstream library authors

Authors of libraries that consume data frames. They can use the API defined in this document
to know how the data contained in a data frame can be consumed, and which operations are implemented.

A non-exhaustive list of downstream library categories is next:

- Plotting and visualization (Matplotlib, Bokeh, Altair, Plotly, etc.)
- Statistical libraries (statsmodels)
- Machine learning libraries (scikit-learn)


### Upstream library authors

Authors of libraries that provide functionality used by data frames.

A non-exhaustive list of upstream categories is next:

- Data interchange protocols (Apache Arrow, NumPy's protocol buffer)
- Mathematical computational libraries (MKL)
- Task schedulers (Dask, Ray)


### Data frame power users

This group considers power users of data frames. For example, developers of applications that
use data frames. Or authors of libraries that provide specialized data frame APIs to be built
on top of the standard API.

Basic users of data frame are not considered direct users of this standard data frame API. This
could include for example users analyzing data in a Jupyter notebook using a data frame implementation.


## High-level API overview




## How to read this document




## How to adopt this API




## Definitions




## References

