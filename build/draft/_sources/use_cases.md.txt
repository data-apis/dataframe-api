# Use cases

## Introduction

This section discusses the use cases considered for the standard dataframe API.

The goals and scope of this API are defined in the [goals](purpose_and_scope.md#Goals),
and [scope](purpose_and_scope.md#Scope) sections.

The target audience and stakeholders are presented in the
[stakeholders](purpose_and_scope.md#Stakeholders) section.


## Types of use cases

The next types of use cases can be accomplished by the use of the standard Python dataframe
API defined in this document:

- Downstream library receiving a dataframe as a parameter
- Converting a dataframe from one implementation to another (try to clarify)

Other types of uses cases not related to data interchange will be added later.


## Concrete use cases

In this section we define concrete examples of the types of use cases defined above.

### Plotting library receiving data as a dataframe

One use case we facilitate with the API defined in this document is a plotting library
receiving the data to be plotted as a dataframe object.

Consider the case of a scatter plot, that will be plotted with the data contained in a
dataframe structure. For example, consider this data:

| petal length | petal width |
|--------------|-------------|
|          1.4 |         0.2 |
|          1.7 |         0.4 |
|          1.3 |         0.2 |
|          1.5 |         0.1 |

If we consider a pure Python implementation, we could for example receive the information
as two lists, one for the _petal length_ and one for the _petal width_.

```python
petal_length = [1.4, 1.7, 1.3, 1.5]
petal_width = [0.2, 0.4, 0.2, 0.1]

def scatter_plot(x: list, y: list):
    """
    Generate a scatter plot with the information provided in `x` and `y`.
    """
    ...
```

When we consider dataframes, we would like to provide them directly to the `scatter_plot`
function. And we would like the plotting library to be agnostic of what specific library
will be used when calling the function. We would like the code to work whether a pandas,
Dask, Vaex or other current or future implementation are used.

An implementation of the `scatter_plot` function could be:

```python
def scatter_plot(data: dataframe, x_column: str, y_column: str):
    """
    Generate a scatter plot with the information provided in `x` and `y`.
    """
    ...
```

The API documented here describes what the developer of the plotting library can expect
from the object `data`. In which ways can interact with the dataframe object to extract
the desired information.

An example of this are Seaborn plots. For example, the
[scatterplot](https://seaborn.pydata.org/generated/seaborn.scatterplot.html) accepts a
parameter `data`, which is expected to be a `DataFrame`.

When providing a pandas `DataFrame`, the next code generates the intended scatter plot:

```python
import pandas
import seaborn

pandas_df = pandas.DataFrame({'bill': [15, 32, 28],
                              'tip': [2, 5, 3]})

seaborn.scatterplot(data=pandas_df, x='bill', y='tip')
```

But if we instead provide a Vaex dataframe, then an exception occurs:

```python
import vaex

vaex_df = vaex.from_pandas(pandas_df)

seaborn.scatterplot(data=vaex_df, x='bill', y='tip')
```

This is caused by Seaborn expecting a pandas `DataFrame` object. And while Vaex
provides an interface very similar to pandas, it does not implement 100% of its
API, and Seaborn is trying to use parts that differ.

With the definition of the standard API, Seaborn developers should be able to
expect a generic dataframe. And any library implementing the standard dataframe
API could be plotted with the previous example (Vaex, cuDF, Ibis, Dask, Modin, etc.).


### Change object from one implementation to another

Another considered use case is transforming the data from one implementation to another.

As an example, consider we are using Dask dataframes, given that our data is too big to
fit in memory, and we are working over a cluster. At some point in our pipeline, we
reduced the size of the dataframe we are working on, by filtering and grouping. And
we are interested in transforming the dataframe from Dask to pandas, to use some
functionalities that pandas implements but Dask does not.

Since Dask knows how the data in the dataframe is represented, one option could be to
implement a `.to_pandas()` method in the Dask dataframe. Another option could be to
implement this in pandas, in a `.from_dask()` method.

As the ecosystem grows, this solution implies that every implementation could end up
having a long list of functions or methods:

- `to_pandas()` / `from_pandas()`
- `to_vaex()` / `from_vaex()`
- `to_modin()` / `from_modin()`
- `to_dask()` / `from_dask()`
- ...

With a standard Python dataframe API, every library could simply implement a method to
import a standard dataframe. And since dataframe libraries are expected to implement
this API, that would be enough to transform any dataframe to one implementation.

So, the list above would be reduced to a single function or method in each implementation:

- `from_dataframe()`

Note that the function `from_dataframe()` is for illustration, and not proposed as part
of the standard at this point.

Every pair of dataframe libraries could benefit from this conversion. But we can go
deeper with an actual example. The conversion from an xarray `DataArray` to a pandas
`DataFrame`, and the other way round.

Even if xarray is not a dataframe library, but a multidimensional labeled structure,
in cases where a 2-D is used, the data can be converted from and to a dataframe.

Currently, xarray implements a `.to_pandas()` method to convert a `DataArray` to a
pandas `DataFrame`:

```python
import xarray

xarray_data = xarray.DataArray([[15, 2], [32, 5], [28, 3]],
                               dims=('diners', 'features'),
                               coords={'features': ['bill', 'tip']})

pandas_df = xarray_data.to_pandas()
```

To convert the pandas dataframe to an xarray `Data Array`, both libraries have
implementations. Both lines below are equivalent:

```python
pandas_df.to_xarray()
xarray.DataArray(pandas_df)
```

Other dataframe implementations may or may not implement a way to convert to xarray.
And passing a dataframe to the `DataArray` constructor may or may not work.

The standard dataframe API would allow pandas, xarray and other libraries to
implement the standard API. They could convert other representations via a single
`from_dataframe()` function or method. And they could be converted to other
representations that implement that function automatically.

This would make conversions very simple, not only among dataframe libraries, but
also among other libraries which data can be expressed as tabular data, such as
xarray, SQLAlchemy and others.
