# Use cases

## Introduction

This section discusses the use cases considered for the standard data frame API.

The goals and scope of this API are defined in the [goals](01_purpose_and_scope.html#Goals),
and [scope](01_purpose_and_scope.html#Scope) sections.

The target audience and stakeholders are presented in the
[stakeholders](01_purpose_and_scope.html#Stakeholders) section.


## Types of use cases

The next types of use cases can be accomplished by the use of the standard Python data frame
API defined in this document:

- Downstream library receiving a data frame as a parameter
- Converting a data frame from one implementation to another
- Other types of uses cases not related to data interchange will be added later


## Concrete use cases

In this section we define concrete examples of the types of use cases defined above.

### Plotting library receiving data as a data frame

One use case we facilitate with the API defined in this document is a plotting library
receiving the data to be plotted as a data frame object.

Consider the case of a scatter plot, that will be plotted with the data contained in a
data frame structure. For example, consider this data:

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

When we consider data frames, we would like to provide them directly to the `scatter_plot`
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
from the object `data`. In which ways can interact with the data frame object to extract
the desired information.


### Change object from one implementation to another

Another considered use case is transforming the data from one implementation to another.

As an example, consider we are using Dask data frames, given that our data is too big to
fit in memory, and we are working over a cluster. At some point in our pipeline, we
reduced the size of the data frame we are working on, by filtering and grouping. And
we are interested in transforming the data frame from Dask to pandas, to use some
functionalities that pandas implements but Dask does not.

Since Dask knows how the data in the data frame is represented, one option could be to
implement a `.to_pandas()` method in the Dask data frame. Another option could be to
implement this in pandas, in a `.from_dask()` method.

As the ecosystem grows, this solution implies that every implementation could end up
having a long list of methods:

- `.to_pandas()` / `.from_pandas()`
- `.to_vaex()` / `.from_vaex()`
- `.to_modin()` / `.from_modin()`
- `.to_dask()` / `.from_dask()`
- ...

With a standard Python data frame API, every library could simply implement a method to
import a standard data frame. And since data frame libraries are expected to implement
this API, that would be enough to transform any data frame to one implementation.

So, the list above would be reduced to a single method in each implementation:

- `.from_dataframe()`

Note that the method `.from_dataframe()` is for illustration, and not proposed as part
of the standard.
