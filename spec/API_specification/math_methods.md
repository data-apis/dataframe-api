# Math Methods

> Dataframe API specification for math methods.

A conforming implementation of the dataframe API standard must provide and support the following methods adhering to the following conventions.

-   Positional parameters must be [positional-only](https://www.python.org/dev/peps/pep-0570/) parameters. Positional-only parameters have no externally-usable name. When a method accepting positional-only parameters is called, positional arguments are mapped to these parameters based solely on their order.
-   Optional parameters must be [keyword-only](https://www.python.org/dev/peps/pep-3102/) arguments.

## Methods

<!-- NOTE: please keep the methods in alphabetical order -->

(method-abs)=
### abs()

Calculates the absolute value for each element of the dataframe instance `df` (i.e., the element-wise result has the same magnitude as the respective element in the original dataframe but has positive sign).

#### Special Cases

For floating-point operands,

-   If an element is `NaN`, the result is `NaN`.
-   If an element is `-0`, the result is `+0`.
-   If an element is `-infinity`, the result is `+infinity`.

#### Returns

-   **out**: _&lt;dataframe&gt;_

    -   dataframe containing element-wise results. Each element of the returned dataframe must have the same data type as the respective element in the original dataframe.

(method-add)=
### add(other, /)

Calculates the sum for each element `df_i` of the dataframe instance `df` with the respective element `other_i` of the dataframe `other`.

#### Special Cases

For floating-point operands,

-   If either `df_i` or `other_i` is `NaN`, the result is `NaN`.
-   If `df_i` is `+infinity` and `other_i` is `-infinity`, the result is `NaN`.
-   If `df_i` is `-infinity` and `other_i` is `+infinity`, the result is `NaN`.
-   If `df_i` is `+infinity` and `other_i` is `+infinity`, the result is `+infinity`.
-   If `df_i` is `-infinity` and `other_i` is `-infinity`, the result is `-infinity`.
-   If `df_i` is `+infinity` and `other_i` is a finite number, the result is `+infinity`.
-   If `df_i` is `-infinity` and `other_i` is a finite number, the result is `-infinity`.
-   If `df_i` is a finite number and `other_i` is `+infinity`, the result is `+infinity`.
-   If `df_i` is a finite number and `other_i` is `-infinity`, the result is `-infinity`.
-   If `df_i` is `-0` and `other_i` is `-0`, the result is `-0`.
-   If `df_i` is `-0` and `other_i` is `+0`, the result is `+0`.
-   If `df_i` is `+0` and `other_i` is `-0`, the result is `+0`.
-   If `df_i` is `+0` and `other_i` is `+0`, the result is `+0`.
-   If `df_i` is either `+0` or `-0` and `other_i` is a nonzero finite number, the result is `other_i`.
-   If `df_i` is a nonzero finite number and `other_i` is either `+0` or `-0`, the result is `df_i`.
-   If `df_i` is a nonzero finite number and `other_i` is `-df_i`, the result is `+0`.
-   In the remaining cases, when neither `infinity`, `+0`, `-0`, nor a `NaN` is involved, and the operands have the same mathematical sign or have different magnitudes, the sum must be computed and rounded to the nearest representable value according to IEEE 754-2019 and a supported round mode. If the magnitude is too large to represent, the operation overflows and the result is an `infinity` of appropriate mathematical sign.

```{note}

Floating-point addition is a commutative operation, but not always associative.
```

#### Parameters

-   **other**: _&lt;dataframe&gt;_

    -   dataframe. Must be compatible with the dataframe instance (**TODO: broadcasting**).

#### Returns

-   **out**: _&lt;dataframe&gt;_

    -   dataframe containing element-wise results. Each element (**FIXME: only numerical elements**) of the returned dataframe must have a data type determined by **TODO: Type Promotion Rules**.

(method-div)=
### div(other, /)

Calculates the division for each element `df_i` of the dataframe instance `df` with the respective element `other_i` of the dataframe `other`.

#### Special Cases

For floating-point operands,

-   If either `df_i` or `other_i` is `NaN`, the result is `NaN`.
-   If `df_i` is either `+infinity` or `-infinity` and `other_i` is either `+infinity` or `-infinity`, the result is `NaN`.
-   If `df_i` is either `+0` or `-0` and `other_i` is either `+0` or `-0`, the result is `NaN`.
-   If `df_i` is `+0` and `other_i` is greater than `0`, the result is `+0`.
-   If `df_i` is `-0` and `other_i` is greater than `0`, the result is `-0`.
-   If `df_i` is `+0` and `other_i` is less than `0`, the result is `-0`.
-   If `df_i` is `-0` and `other_i` is less than `0`, the result is `+0`.
-   If `df_i` is greater than `0` and `other_i` is `+0`, the result is `+infinity`.
-   If `df_i` is greater than `0` and `other_i` is `-0`, the result is `-infinity`.
-   If `df_i` is less than `0` and `other_i` is `+0`, the result is `-infinity`.
-   If `df_i` is less than `0` and `other_i` is `-0`, the result is `+infinity`.
-   If `df_i` is `+infinity` and `other_i` is a positive (i.e., greater than `0`) finite number, the result is `+infinity`.
-   If `df_i` is `+infinity` and `other_i` is a negative (i.e., less than `0`) finite number, the result is `-infinity`.
-   If `df_i` is `-infinity` and `other_i` is a positive (i.e., greater than `0`) finite number, the result is `-infinity`.
-   If `df_i` is `-infinity` and `other_i` is a negative (i.e., less than `0`) finite number, the result is `+infinity`.
-   If `df_i` is a positive (i.e., greater than `0`) finite number and `other_i` is `+infinity`, the result is `+0`.
-   If `df_i` is a positive (i.e., greater than `0`) finite number and `other_i` is `-infinity`, the result is `-0`.
-   If `df_i` is a negative (i.e., less than `0`) finite number and `other_i` is `+infinity`, the result is `-0`.
-   If `df_i` is a negative (i.e., less than `0`) finite number and `other_i` is `-infinity`, the result is `+0`.
-   If `df_i` and `other_i` have the same mathematical sign and are both nonzero finite numbers, the result has a positive mathematical sign.
-   If `df_i` and `other_i` have different mathematical signs and are both nonzero finite numbers, the result has a negative mathematical sign.
-   In the remaining cases, where neither `-infinity`, `+0`, `-0`, nor `NaN` is involved, the quotient must be computed and rounded to the nearest representable value according to IEEE 754-2019 and a supported rounding mode. If the magnitude is too larger to represent, the operation overflows and the result is an `infinity` of appropriate mathematical sign. If the magnitude is too small to represent, the operation underflows and the result is a zero of appropriate mathematical sign.

#### Parameters

-   **other**: _&lt;dataframe&gt;_

    -   divisor dataframe. Must be compatible with the dataframe instance (**TODO: broadcasting**).

#### Returns

-   **out**: _&lt;dataframe&gt;_

    -   dataframe containing element-wise results. Each element (**FIXME: only numerical elements**) of the returned dataframe must have a floating-point data type determined by **TODO: Type Promotion Rules**.

(method-floordiv)=
### floordiv(other, /)

Rounds the result of dividing each element `df_i` of the dataframe instance `df` by the respective element `other_i` of the dataframe `other` to the greatest (i.e., closest to `+infinity`) integer-value number that is not greater than the division result.

#### Parameters

-   **other**: _&lt;dataframe&gt;_

    -   divisor dataframe. Must be compatible with the dataframe instance (**TODO: broadcasting**).

#### Returns

-   **out**: _&lt;dataframe&gt;_

    -   dataframe containing element-wise results. Each element (**FIXME: only numerical elements**) of the returned dataframe must have a data type determined by **TODO: Type Promotion Rules**.

(method-mod)=
### mod(other, /)

Calculates the remainder of division for each element `df_i` of the dataframe instance `df` with the respective element `other_i` of the dataframe `other`.

#### Parameters

-   **other**: _&lt;dataframe&gt;_

    -   divisor dataframe. Must be compatible with the dataframe instance (**TODO: broadcasting**).

#### Returns

-   **out**: _&lt;dataframe&gt;_

    -   dataframe containing element-wise results. Each element-wise result must have the same sign as the respective element `other_i`. Each element (**FIXME: only numerical elements**) of the returned dataframe must have a floating-point data type determined by **TODO: Type Promotion Rules**.

(method-mul)=
### mul(other, /)

Calculates the product for each element `df_i` of the dataframe instance `df` with the respective element `other_i` of the dataframe `other`.

#### Special Cases

For floating-point operands,

-   If either `df_i` or `other_i` is `NaN`, the result is `NaN`.
-   If `df_i` is either `+infinity` or `-infinity` and `other_i` is either `+0` or `-0`, the result is `NaN`.
-   If `df_i` is either `+0` or `-0` and `other_i` is either `+infinity` or `-infinity`, the result is `NaN`.
-   If `df_i` and `other_i` have the same mathematical sign, the result has a positive mathematical sign, unless the result is `NaN`. If the result is `NaN`, the "sign" of `NaN` is implementation-defined.
-   If `df_i` and `other_i` have different mathematical signs, the result has a negative mathematical sign, unless the result is `NaN`. If the result is `NaN`, the "sign" of `NaN` is implementation-defined.
-   If `df_i` is either `+infinity` or `-infinity` and `other_i` is either `+infinity` or `-infinity`, the result is a signed infinity with the mathematical sign determined by the rule already stated above.
-   If `df_i` is either `+infinity` or `-infinity` and `other_i` is a nonzero finite number, the result is a signed infinity with the mathematical sign determined by the rule already stated above.
-   If `df_i` is a nonzero finite number and `other_i` is either `+infinity` or `-infinity`, the result is a signed infinity with the mathematical sign determined by the rule already stated above.
-   In the remaining cases, where neither `infinity` nor `NaN` is involved, the product must be computed and rounded to the nearest representable value according to IEEE 754-2019 and a supported rounding mode. If the magnitude is too large to represent, the result is an `infinity` of appropriate mathematical sign. If the magnitude is too small to represent, the result is a zero of appropriate mathematical sign.

```{note}

Floating-point multiplication is not always associative due to finite precision.
```

#### Parameters

-   **other**: _&lt;dataframe&gt;_

    -   dataframe. Must be compatible with the dataframe instance (**TODO: broadcasting**).

#### Returns

-   **out**: _&lt;dataframe&gt;_

    -   dataframe containing element-wise results. Each element (**FIXME: only numerical elements**) of the returned dataframe must have a data type determined by **TODO: Type Promotion Rules**.

(method-pow)=
### pow(other, /)

Calculates an implementation-dependent approximation of exponentiation by raising each element `df_i` (the base) of the dataframe instance `df` to the power of `other_i` (the exponent), where `other_i` is the corresponding element of the dataframe `other`.

#### Special Cases

For floating-point operands,

-   If `df_i` is not equal to `1` and `other_i` is `NaN`, the result is `NaN`.
-   If `other_i` is `+0`, the result is `1`, even if `df_i` is `NaN`.
-   If `other_i` is `-0`, the result is `1`, even if `df_i` is `NaN`.
-   If `df_i` is `NaN` and `other_i` is not equal to `0`, the result is `NaN`.
-   If `abs(df_i)` is greater than `1` and `other_i` is `+infinity`, the result is `+infinity`.
-   If `abs(df_i)` is greater than `1` and `other_i` is `-infinity`, the result is `+0`.
-   If `abs(df_i)` is `1` and `other_i` is `+infinity`, the result is `1`.
-   If `abs(df_i)` is `1` and `other_i` is `-infinity`, the result is `1`.
-   If `df_i` is `1` and `other_i` is not `NaN`, the result is `1`.
-   If `abs(df_i)` is less than `1` and `other_i` is `+infinity`, the result is `+0`.
-   If `abs(df_i)` is less than `1` and `other_i` is `-infinity`, the result is `+infinity`.
-   If `df_i` is `+infinity` and `other_i` is greater than `0`, the result is `+infinity`.
-   If `df_i` is `+infinity` and `other_i` is less than `0`, the result is `+0`.
-   If `df_i` is `-infinity` and `other_i` is greater than `0`, the result is `-infinity`.
-   If `df_i` is `-infinity`, `other_i` is greater than `0`, and `other_i` is not an odd integer value, the result is `+infinity`.
-   If `df_i` is `-infinity`, `other_i` is less than `0`, and `other_i` is an odd integer value, the result is `-0`.
-   If `df_i` is `-infinity`, `other_i` is less than `0`, and `other_i` is not an odd integer value, the result is `+0`.
-   If `df_i` is `+0` and `other_i` is greater than `0`, the result is `+0`.
-   If `df_i` is `+0` and `other_i` is less than `0`, the result is `+infinity`.
-   If `df_i` is `-0`, `other_i` is greater than `0`, and `other_i` is an odd integer value, the result is `-0`.
-   If `df_i` is `-0`, `other_i` is greater than `0`, and `other_i` is not an odd integer value, the result is `+0`.
-   If `df_i` is `-0`, `other_i` is less than `0`, and `other_i` is an odd integer value, the result is `-infinity`.
-   If `df_i` is `-0`, `other_i` is less than `0`, and `other_i` is not an odd integer value, the result is `+infinity`.
-   If `df_i` is less than `0`, `df_i` is a finite number, `other_i` is a finite number, and `other_i` is not an integer value, the result is `NaN`.

#### Parameters

-   **other**: _&lt;dataframe&gt;_

    -   dataframe whose elements correspond to the exponentiation exponent. Must be compatible with the dataframe instance (**TODO: broadcasting**).

#### Returns

-   **out**: _&lt;dataframe&gt;_

    -   dataframe containing element-wise results. Each element (**FIXME: only numerical elements**) of the returned dataframe must have a data type determined by **TODO: Type Promotion Rules**.

(method-sub)=
### sub(other, /)

Calculates the difference for each element `df_i` of the dataframe instance `df` with the respective element `other_i` of the dataframe `other`. The result of `df_i - other_i` must be the same as `df_i + (-other_i)` and must be governed by the same floating-point rules as addition (see `add()`).

#### Parameters

-   **other**: _&lt;dataframe&gt;_

    -   dataframe. Must be compatible with the dataframe instance (**TODO: broadcasting**).

#### Returns

-   **out**: _&lt;dataframe&gt;_

    -   dataframe containing element-wise results. Each element (**FIXME: only numerical elements**) of the returned dataframe must have a data type determined by **TODO: Type Promotion Rules**.