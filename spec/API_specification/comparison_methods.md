# Comparison Methods

> Dataframe API specification for comparison methods.

A conforming implementation of the dataframe API standard must provide and support the following methods adhering to the following conventions.

-   Positional parameters must be [positional-only](https://www.python.org/dev/peps/pep-0570/) parameters. Positional-only parameters have no externally-usable name. When a method accepting positional-only parameters is called, positional arguments are mapped to these parameters based solely on their order.
-   Optional parameters must be [keyword-only](https://www.python.org/dev/peps/pep-3102/) arguments.

## Methods

<!-- NOTE: please keep the methods in alphabetical order -->

(method-eq)=
### eq(other, /, *, axis=None)

Computes the truth value of `df_i == other_i` for each element `df_i` of the dataframe instance `df` with the respective element `other_i` of the dataframe `other`.

#### Parameters

-   **other**: _&lt;dataframe&gt;_

    -   dataframe. Must be compatible with the dataframe instance (**TODO: broadcasting**).

-   **axis**: _Optional\[ int ]_

    -   axis along which to compare. If equal to `0`, element-wise comparison must be performed over the index. If equal to `1`, element-wise comparison must be performed over the columns. By default, element-wise comparison must be computed over the columns. Default: `None`.

#### Returns

-   **out**: _&lt;dataframe&gt;_

    -   dataframe containing element-wise results. Each element of the returned dataframe must be of type `bool`.

(method-ge)=
### ge(other, /, *, axis=None)

Computes the truth value of `df_i >= other_i` for each element `df_i` of the dataframe instance `df` with the respective element `other_i` of the dataframe `other`.

#### Parameters

-   **other**: _&lt;dataframe&gt;_

    -   dataframe. Must be compatible with the dataframe instance (**TODO: broadcasting**).

-   **axis**: _Optional\[ int ]_

    -   axis along which to compare. If equal to `0`, element-wise comparison must be performed over the index. If equal to `1`, element-wise comparison must be performed over the columns. By default, element-wise comparison must be computed over the columns. Default: `None`.

#### Returns

-   **out**: _&lt;dataframe&gt;_

    -   dataframe containing element-wise results. Each element of the returned dataframe must be of type `bool`.

(method-gt)=
### gt(other, /, *, axis=None)

Computes the truth value of `df_i > other_i` for each element `df_i` of the dataframe instance `df` with the respective element `other_i` of the dataframe `other`.

#### Parameters

-   **other**: _&lt;dataframe&gt;_

    -   dataframe. Must be compatible with the dataframe instance (**TODO: broadcasting**).

-   **axis**: _Optional\[ int ]_

    -   axis along which to compare. If equal to `0`, element-wise comparison must be performed over the index. If equal to `1`, element-wise comparison must be performed over the columns. By default, element-wise comparison must be computed over the columns. Default: `None`.

#### Returns

-   **out**: _&lt;dataframe&gt;_

    -   dataframe containing element-wise results. Each element of the returned dataframe must be of type `bool`.

(method-le)=
### le(other, /, *, axis=None)

Computes the truth value of `df_i <= other_i` for each element `df_i` of the dataframe instance `df` with the respective element `other_i` of the dataframe `other`.

#### Parameters

-   **other**: _&lt;dataframe&gt;_

    -   dataframe. Must be compatible with the dataframe instance (**TODO: broadcasting**).

-   **axis**: _Optional\[ int ]_

    -   axis along which to compare. If equal to `0`, element-wise comparison must be performed over the index. If equal to `1`, element-wise comparison must be performed over the columns. By default, element-wise comparison must be computed over the columns. Default: `None`.

#### Returns

-   **out**: _&lt;dataframe&gt;_

    -   dataframe containing element-wise results. Each element of the returned dataframe must be of type `bool`.

(method-lt)=
### lt(other, /, *, axis=None)

Computes the truth value of `df_i < other_i` for each element `df_i` of the dataframe instance `df` with the respective element `other_i` of the dataframe `other`.

#### Parameters

-   **other**: _&lt;dataframe&gt;_

    -   dataframe. Must be compatible with the dataframe instance (**TODO: broadcasting**).

-   **axis**: _Optional\[ int ]_

    -   axis along which to compare. If equal to `0`, element-wise comparison must be performed over the index. If equal to `1`, element-wise comparison must be performed over the columns. By default, element-wise comparison must be computed over the columns. Default: `None`.

#### Returns

-   **out**: _&lt;dataframe&gt;_

    -   dataframe containing element-wise results. Each element of the returned dataframe must be of type `bool`.

(method-ne)=
### ne(other, /, *, axis=None)

Computes the truth value of `df_i != other_i` for each element `df_i` of the dataframe instance `df` with the respective element `other_i` of the dataframe `other`.

#### Parameters

-   **other**: _&lt;dataframe&gt;_

    -   dataframe. Must be compatible with the dataframe instance (**TODO: broadcasting**).

-   **axis**: _Optional\[ int ]_

    -   axis along which to compare. If equal to `0`, element-wise comparison must be performed over the index. If equal to `1`, element-wise comparison must be performed over the columns. By default, element-wise comparison must be computed over the columns. Default: `None`.

#### Returns

-   **out**: _&lt;dataframe&gt;_

    -   dataframe containing element-wise results. Each element of the returned dataframe must be of type `bool`.