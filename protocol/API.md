# API of the `__dataframe__` protocol

Specification for objects to be accessed, for the purpose of dataframe
interchange between libraries, via the `__dataframe__` method on a libraries'
data frame object.

For guiding requirements, see {ref}`design-requirements`.


## Concepts in this design

1. A `Buffer` class. A *buffer* is a contiguous block of memory - this is the
   only thing that actually maps to a 1-D array in a sense that it could be
   converted to NumPy, CuPy, et al.
2. A `Column` class. A *column* has a single dtype. It can consist
   of multiple *chunks*. A single chunk of a column (which may be the whole
   column if ``num_chunks == 1``) is modeled as again a `Column` instance, and
   contains 1 data *buffer* and (optionally) one *mask* for missing data.
3. A `DataFrame` class. A *data frame* is an ordered collection of *columns*,
   which are identified with names that are unique strings.  All the data
   frame's rows are the same length. It can consist of multiple *chunks*. A
   single chunk of a data frame is modeled as again a `DataFrame` instance.
4. A *mask* concept. A *mask* of a single-chunk column is a *buffer*.
5. A *chunk* concept. A *chunk* is a sub-dividing element that can be applied
   to a *data frame* or a *column*.

Note that the only way to access these objects is through a call to
`__dataframe__` on a data frame object. This is NOT meant as public API;
only think of instances of the different classes here to describe the API of
what is returned by a call to `__dataframe__`. They are the concepts needed
to capture the memory layout and data access of a data frame.


## Design decisions

1. Use a separate column abstraction in addition to a dataframe interface.

   Rationales:

   - This is how it works in R, Julia and Apache Arrow.
   - Semantically most existing applications and users treat a column similar to a 1-D array
   - We should be able to connect a column to the array data interchange mechanism(s)

   Note that this does not imply a library must have such a public user-facing
   abstraction (ex. ``pandas.Series``) - it can only be accessed via
   ``__dataframe__``.

2. Use methods and properties on an opaque object rather than returning
   hierarchical dictionaries describing memory.

   This is better for implementations that may rely on, for example, lazy
   computation.

3. No row names. If a library uses row names, use a regular column for them.

   See discussion at
   [wesm/dataframe-protocol/pull/1](https://github.com/wesm/dataframe-protocol/pull/1/files#r394316241)
   Optional row names are not a good idea, because people will assume they're
   present (see cuDF experience, forced to add because pandas has them).
   Requiring row names seems worse than leaving them out.  Note that row labels
   could be added in the future - right now there's no clear requirements for
   more complex row labels that cannot be represented by a single column. These
   do exist, for example Modin has has table and tree-based row labels.

## Interface



```{literalinclude} dataframe_protocol.py
---
language: python
---
