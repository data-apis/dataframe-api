# `__dataframe__` protocol - summary

_We've had a lot of discussion in a couple of GitHub issues and in meetings.
This description attempts to summarize that, and extract the essential design
requirements/principles and functionality it needs to support._

## Purpose of `__dataframe__`

The purpose of `__dataframe__` is to be a _data interchange_ protocol. I.e.,
a way to convert one type of dataframe into another type (for example,
convert a Koalas dataframe into a Pandas dataframe, or a cuDF dataframe into
a Vaex dataframe).

Currently (Nov'20) there is no way to do this in an implementation-independent way.

The main use case this protocol intends to enable is to make it possible to
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

### Non-goals

Providing a _complete standardized dataframe API_ is not a goal of the
`__dataframe__` protocol. Instead, this is a goal of the full dataframe API
standard, which the Consortium for Python Data API Standards aims to provide
in the future. When that full API standard is implemented by dataframe
libraries, the example above can change to:

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


## Protocol design requirements

1. Must be a standard Python-level API that is unambiguously specified, and
   not rely on implementation details of any particular dataframe library.
2. Must treat dataframes as a collection of columns (which are 1-D arrays
   with a dtype and missing data support).
   _Note: this related to the API for `__dataframe__`, and does not imply
   that the underlying implementation must use columnar storage!_
3. Must allow the consumer to select a specific set of columns for conversion.
4. Must allow the consumer to access the following "metadata" of the dataframe:
   number of rows, number of columns, column names, column data types.
   TBD: column data types wasn't clearly decided on, nor is it present in https://github.com/wesm/dataframe-protocol
5. Must include device support
6. Must avoid device transfers by default (e.g. copy data from GPU to CPU),
   and provide an explicit way to force such transfers (e.g. a `force=` or
   `copy=` keyword that the caller can set to `True`).
7. Must be zero-copy if possible.
8. Must be able to support "virtual columns" (e.g., a library like Vaex which
   may not have data in memory because it uses lazy evaluation).
9. Must support missing values (`NA`) for all supported dtypes.
10. Must supports string and categorical dtypes

We'll also list some things that were discussed but are not requirements:

1. Object dtype does not need to be supported
2. Heterogeneous/structured dtypes within a single column does not need to be
   supported.
   _Rationale: not used a lot, additional design complexity not justified._


## Frequently asked questions

### Can the Arrow C Data Interface be used for this?

What we are aiming for is quite similar to the Arrow C Data Interface (see
the [rationale for the Arrow C Data Interface](https://arrow.apache.org/docs/format/CDataInterface.html#rationale)),
except `__dataframe__` is a Python-level rather than C-level interface.
_TODO: one key thing is Arrow C Data interface relies on providing a deletion
/ finalization method similar to DLPack. The desired semantics here need to
be ironed out. See Arrow docs on [release callback semantics](https://arrow.apache.org/docs/format/CDataInterface.html#release-callback-semantics-for-consumers)_

The main (only?) limitation seems to be:
- No device support (@kkraus14 will bring this up on the Arrow dev mailing list)

Note that categoricals are supported, Arrow uses the phrasing
"dictionary-encoded types" for categorical.

The Arrow C Data Interface says specifically it was inspired by [Python's
buffer protocol](https://docs.python.org/3/c-api/buffer.html), which is also
a C-only and CPU-only interface. See `__array_interface__` below for a
Python-level equivalent of the buffer protocol.


### Is `__dataframe__` analogous to `__array__` or `__array_interface__`?

Yes, it is fairly analogous to `__array_interface__`. There will be some
differences though, for example `__array_interface__` doesn't know about
devices, and it's a `dict` with a pointer to memory so there's an assumption
that the data lives in CPU memory (which may not be true, e.g. in the case of
cuDF or Vaex).

It is _not_ analogous to `__array__`, which is NumPy-specific. `__array__` is a
method attached to array/tensor-like objects, and calling it is requesting
the object it's attached to to turn itself into a NumPy array. Hence, the
library that implements `__array__` must depend (optionally at least) on
NumPy, and call a NumPy `ndarray` constructor itself from within `__array__`.


### What is wrong with `.to_numpy?` and `.to_arrow()`? 

Such methods ask the object it is attached to to turn itself into a NumPy or
Arrow array. Which means each library must have at least an optional
dependency on NumPy and on Arrow if it implements those methods. This leads
to unnecessary coupling between libraries, and hence is a suboptimal choice -
we'd like to avoid this if we can.

Instead, it should be dataframe consumers that rely on NumPy or Arrow, since
they are the ones that need such a particular format. So, it can call the
constructor it needs. For example, `x = np.asarray(df['colname'])` (where
`df` supports `__dataframe__`).


### Does an interface describing memory work for virtual columns?

Vaex is an example of a library that can have "virtual columns" (see @maartenbreddels
[comment here](https://github.com/data-apis/dataframe-api/issues/29#issuecomment-686373569)).
If the protocol includes a description of data layout in memory, does that
work for such a virtual column?

Yes. Virtual columns need to be materialized in memory before they can be
turned into a column for a different type of dataframe - that will be true
for every discussed form of the protocol; whether there's a `to_arrow()` or
something else does not matter. Vaex can choose _how_ to materialize (e.g.,
to an Arrow array, a NumPy array, or a raw memory buffer) - as long as the
returned description of memory layout is valid, all those options can later
be turned into the desired column format without a data copy, so the
implementation choice here really doesn't matter much.

_Note: the above statement on materialization assumes that there are many
forms a virtual column can be implemented, and that those are all
custom/different and that at this point it makes little sense to standardize
that. For example, one could do this with a simple string DSL (`'col_C =
col_A + col_B'`, with a fancier C++-style lazy evaluation, with a
computational graph approach like Dask uses, etc.)._


## Possible direction for implementation

The `cuDFDataFrame`, `cuDFColumn` and `cuDFBuffer` sketched out by @kkraus14
[here](https://github.com/data-apis/dataframe-api/issues/29#issuecomment-685123386)
seems to be in the right direction.

TODO: work this out after making sure we're all on the same page regarding requirements.
