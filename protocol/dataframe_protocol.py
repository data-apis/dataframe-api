"""
Specification for objects to be accessed, for the purpose of dataframe
interchange between libraries, via the ``__dataframe__`` method on a libraries'
data frame object.

For guiding requirements, see https://github.com/data-apis/dataframe-api/pull/35


Concepts in this design
-----------------------

1. A `Buffer` class. A *buffer* is a contiguous block of memory - this is the
  only thing that actually maps to a 1-D array in a sense that it could be
  converted to NumPy, CuPy, et al.
2. A `Column` class. A *column* has a name and a single dtype. It can consist
   of multiple *chunks*. A single chunk of a column (which may be the whole
   column if ``num_chunks == 1``) is modeled as again a `Column` instance, and
   contains 1 data *buffer* and (optionally) one *mask* for missing data.
3. A `DataFrame` class. A *data frame* is an ordered collection of *columns*.
   It has a single device, and all its rows are the same length. It can consist
   of multiple *chunks*. A single chunk of a data frame is modeled as
   again a `DataFrame` instance.
4. A *mask* concept. A *mask* of a single-chunk column is a *buffer*.
5. A *chunk* concept. A *chunk* is a sub-dividing element that can be applied
   to a *data frame* or a *column*.

Note that the only way to access these objects is through a call to
``__dataframe__`` on a data frame object. This is NOT meant as public API;
only think of instances of the different classes here to describe the API of
what is returned by a call to ``__dataframe__``. They are the concepts needed
to capture the memory layout and data access of a data frame.


Design decisions
----------------

**1. Use a separate column abstraction in addition to a dataframe interface.**

Rationales:
- This is how it works in R, Julia and Apache Arrow.
- Semantically most existing applications and users treat a column similar to a 1-D array
- We should be able to connect a column to the array data interchange mechanism(s)

Note that this does not imply a library must have such a public user-facing
abstraction (ex. ``pandas.Series``) - it can only be accessed via ``__dataframe__``.

**2. Use methods and properties on an opaque object rather than returning
hierarchical dictionaries describing memory**

This is better for implementations that may rely on, for example, lazy
computation.

**3. No row names. If a library uses row names, use a regular column for them.**

See discussion at https://github.com/wesm/dataframe-protocol/pull/1/files#r394316241
Optional row names are not a good idea, because people will assume they're present
(see cuDF experience, forced to add because pandas has them).
Requiring row names seems worse than leaving them out.

Note that row labels could be added in the future - right now there's no clear
requirements for more complex row labels that cannot be represented by a single
column. That do exist, for example Modin has has table and tree-based row
labels.

"""


class Buffer:
    """
    Data in the buffer is guaranteed to be contiguous in memory.

    Note that there is no dtype attribute present, a buffer can be thought of
    as simply a block of memory. However, if the column that the buffer is
    attached to has a dtype that's supported by DLPack and ``__dlpack__`` is
    implemented, then that dtype information will be contained in the return
    value from ``__dlpack__``.

    This distinction is useful to support both data exchange via DLPack on a
    buffer and (b) dtypes like variable-length strings which do not have a
    fixed number of bytes per element.
    """

    @property
    def bufsize(self) -> int:
        """
        Buffer size in bytes
        """
        pass

    @property
    def ptr(self) -> int:
        """
        Pointer to start of the buffer as an integer
        """
        pass

    def __dlpack__(self):
        """
        Produce DLPack capsule (see array API standard).

        Raises:

            - TypeError : if the buffer contains unsupported dtypes.
            - NotImplementedError : if DLPack support is not implemented

        Useful to have to connect to array libraries. Support optional because
        it's not completely trivial to implement for a Python-only library.
        """
        raise NotImplementedError("__dlpack__")

    def __dlpack_device__(self) -> Tuple[enum.IntEnum, int]:
        """
        Device type and device ID for where the data in the buffer resides.

        Uses device type codes matching DLPack. Enum members are::

            - CPU = 1
            - CUDA = 2
            - CPU_PINNED = 3
            - OPENCL = 4
            - VULKAN = 7
            - METAL = 8
            - VPI = 9
            - ROCM = 10

        Note: must be implemented even if ``__dlpack__`` is not.
        """
        pass


class Column:
    """
    A column object, with only the methods and properties required by the
    interchange protocol defined.

    A column can contain one or more chunks. Each chunk can contain either one
    or two buffers - one data buffer and (depending on null representation) it
    may have a mask buffer.

    TBD: Arrow has a separate "null" dtype, and has no separate mask concept.
         Instead, it seems to use "children" for both columns with a bit mask,
         and for nested dtypes. Unclear whether this is elegant or confusing.
         This design requires checking the null representation explicitly.

         The Arrow design requires checking:
         1. the ARROW_FLAG_NULLABLE (for sentinel values)
         2. if a column has two children, combined with one of those children
            having a null dtype.

         Making the mask concept explicit seems useful. One null dtype would
         not be enough to cover both bit and byte masks, so that would mean
         even more checking if we did it the Arrow way.

    TBD: there's also the "chunk" concept here, which is implicit in Arrow as
         multiple buffers per array (= column here). Semantically it may make
         sense to have both: chunks were meant for example for lazy evaluation
         of data which doesn't fit in memory, while multiple buffers per column
         could also come from doing a selection operation on a single
         contiguous buffer.

         Given these concepts, one would expect chunks to be all of the same
         size (say a 10,000 row dataframe could have 10 chunks of 1,000 rows),
         while multiple buffers could have data-dependent lengths. Not an issue
         in pandas if one column is backed by a single NumPy array, but in
         Arrow it seems possible.
         Are multiple chunks *and* multiple buffers per column necessary for
         the purposes of this interchange protocol, or must producers either
         reuse the chunk concept for this or copy the data?

    Note: this Column object can only be produced by ``__dataframe__``, so
          doesn't need its own version or ``__column__`` protocol.

    """

    @property
    def size(self) -> Optional[int]:
        """
        Size of the column, in elements.

        Corresponds to DataFrame.num_rows() if column is a single chunk;
        equal to size of this current chunk otherwise.
        """
        pass

    @property
    def offset(self) -> int:
        """
        Offset of first element

        May be > 0 if using chunks; for example for a column with N chunks of
        equal size M (only the last chunk may be shorter),
        ``offset = n * M``, ``n = 0 .. N-1``.
        """
        pass

    @property
    def dtype(self) -> Tuple[int, int, str, str]:
        """
        Dtype description as a tuple ``(kind, bit-width, format string, endianness)``

        Kind :

            - 0 : signed integer
            - 1 : unsigned integer
            - 2 : IEEE floating point
            - 20 : boolean
            - 21 : string (UTF-8)
            - 22 : datetime
            - 23 : categorical

        Bit-width : the number of bits as an integer
        Format string : data type description format string in Apache Arrow C
                        Data Interface format.
        Endianness : current only native endianness (``=``) is supported

        Notes:

            - Kind specifiers are aligned with DLPack where possible (hence the
              jump to 20, leave enough room for future extension)
            - Masks must be specified as boolean with either bit width 1 (for bit
              masks) or 8 (for byte masks).
            - Dtype width in bits was preferred over bytes
            - Endianness isn't too useful, but included now in case in the future
              we need to support non-native endianness
            - Went with Apache Arrow format strings over NumPy format strings
              because they're more complete from a dataframe perspective
            - Format strings are mostly useful for datetime specification, and
              for categoricals.
            - For categoricals, the format string describes the type of the
              categorical in the data buffer. In case of a separate encoding of
              the categorical (e.g. an integer to string mapping), this can
              be derived from ``self.describe_categorical``.
            - Data types not included: complex, Arrow-style null, binary, decimal,
              and nested (list, struct, map, union) dtypes.
        """
        pass

    @property
    def describe_categorical(self) -> dict[bool, bool, Optional[dict]]:
        """
        If the dtype is categorical, there are two options:

        - There are only values in the data buffer.
        - There is a separate dictionary-style encoding for categorical values.

        Raises RuntimeError if the dtype is not categorical

        Content of returned dict:

            - "is_ordered" : bool, whether the ordering of dictionary indices is
                             semantically meaningful.
            - "is_dictionary" : bool, whether a dictionary-style mapping of
                                categorical values to other objects exists
            - "mapping" : dict, Python-level only (e.g. ``{int: str}``).
                          None if not a dictionary-style categorical.

        TBD: are there any other in-memory representations that are needed?
        """
        pass

    @property
    def describe_null(self) -> Tuple[int, Any]:
        """
        Return the missing value (or "null") representation the column dtype
        uses, as a tuple ``(kind, value)``.

        Kind:

            - 0 : non-nullable
            - 1 : NaN/NaT
            - 2 : sentinel value
            - 3 : bit mask
            - 4 : byte mask

        Value : if kind is "sentinel value", the actual value. None otherwise.
        """
        pass

    @property
    def null_count(self) -> Optional[int]:
        """
        Number of null elements, if known.

        Note: Arrow uses -1 to indicate "unknown", but None seems cleaner.
        """
        pass

    def num_chunks(self) -> int:
        """
        Return the number of chunks the column consists of.
        """
        pass

    def get_chunks(self, n_chunks : Optional[int] = None) -> Iterable[Column]:
        """
        Return an iterator yielding the chunks.

        See `DataFrame.get_chunks` for details on ``n_chunks``.
        """
        pass

    def get_data_buffer(self) -> Buffer:
        """
        Return the buffer containing the data.
        """
        pass

    def get_mask(self) -> Buffer:
        """
        Return the buffer containing the mask values indicating missing data.

        Raises RuntimeError if null representation is not a bit or byte mask.
        """
        pass

#    # NOTE: not needed unless one considers nested dtypes
#    def get_children(self) -> Iterable[Column]:
#        """
#        Children columns underneath the column, each object in this iterator
#        must adhere to the column specification
#        """
#        pass


class DataFrame:
    """
    A data frame class, with only the methods required by the interchange
    protocol defined.

    A "data frame" represents an ordered collection of named columns.
    A column's "name" must be a unique string.
    Columns may be accessed by name or by position.

    This could be a public data frame class, or an object with the methods and
    attributes defined on this DataFrame class could be returned from the
    ``__dataframe__`` method of a public data frame class in a library adhering
    to the dataframe interchange protocol specification.
    """
    def __dataframe__(self, nan_as_null : bool = False) -> dict:
        """
        Produces a dictionary object following the dataframe protocol spec

        ``nan_as_null`` is a keyword intended for the consumer to tell the
        producer to overwrite null values in the data with ``NaN`` (or ``NaT``).
        It is intended for cases where the consumer does not support the bit
        mask or byte mask that is the producer's native representation.
        """
        self._nan_as_null = nan_as_null
        return {
            "dataframe": self,  # DataFrame object adhering to the protocol
            "version": 0        # Version number of the protocol
        }

    def num_columns(self) -> int:
        """
        Return the number of columns in the DataFrame
        """
        pass

    def num_rows(self) -> Optional[int]:
        # TODO: not happy with Optional, but need to flag it may be expensive
        #       why include it if it may be None - what do we expect consumers
        #       to do here?
        """
        Return the number of rows in the DataFrame, if available
        """
        pass

    def num_chunks(self) -> int:
        """
        Return the number of chunks the DataFrame consists of
        """
        pass

    def column_names(self) -> Iterable[str]:
        """
        Return an iterator yielding the column names.
        """
        pass

    def get_column(self, i: int) -> Column:
        """
        Return the column at the indicated position.
        """
        pass

    def get_column_by_name(self, name: str) -> Column:
        """
        Return the column whose name is the indicated name.
        """
        pass

    def get_columns(self) -> Iterable[Column]:
        """
        Return an iterator yielding the columns.
        """
        pass

    def select_columns(self, indices: Sequence[int]) -> DataFrame:
        """
        Create a new DataFrame by selecting a subset of columns by index
        """
        pass

    def select_columns_by_name(self, names: Sequence[str]) -> DataFrame:
        """
        Create a new DataFrame by selecting a subset of columns by name.
        """
        pass

    def get_chunks(self, n_chunks : Optional[int] = None) -> Iterable[DataFrame]:
        """
        Return an iterator yielding the chunks.

        By default (None), yields the chunks that the data is stored as by the
        producer. If given, ``n_chunks`` must be a multiple of
        ``self.num_chunks()``, meaning the producer must subdivide each chunk
        before yielding it.
        """
        pass

