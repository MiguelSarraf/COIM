# COIM

Constrain Operator for Inferential Models is a simple tool for pre and pos processing of data to eliminate redunduncy in datasets caused by dependency rules between the variables/columns.

# Status

![PyPI - Version](https://img.shields.io/pypi/v/COIM)
![PyPI - License](https://img.shields.io/pypi/l/COIM)
![PyPI - Status](https://img.shields.io/pypi/status/COIM)
![GitHub commits since tagged version](https://img.shields.io/github/commits-since/MiguelSarraf/COIM/v0.0.2)
![GitHub milestone details](https://img.shields.io/github/milestones/progress-percent/MiguelSarraf/COIM/1)
![PyPI - Downloads](https://img.shields.io/pypi/dm/COIM)
![GitHub repo size](https://img.shields.io/github/repo-size/MiguelSarraf/COIM)
![Static Badge](https://img.shields.io/badge/pytest-100%25-green)

## Usage

To start using COIM, import into your code the operator class, which orquestrates the constrains, and define an instance of it.

```
from COIM import ConstrainOperator
operator=ConstrainOperator()
```

To add a new constrain, use the _add\_rule_ method from ConstrainOperator class.

```
from COIM import SomeConstrain
contraint_some_rule=SomeConstrain(**parameters)
operator.add_rule(contraint_some_rule)
```

Each constrain will require their own specific set of parameters, refer to section _Available constrains_ to know each of them. However, all constrains receive the parameter "labels", which is a list with the new names to be used on the encoded columns, and a parameter "precision", which indicates the precision for dataset validation (default to 1e-10).

Then you can encode your dataframe to use the new corrected variables to feed your model.

```encoded_df=operator.encode_dataframe(df)```

After running your model, you can regenerate the data in the original format, decoding the acquired values and errors.

```decoded_df, decoded_errors=operator.decode_dataframe(predicted_df, errors)```

That will yield the predictions for the original variables as if they had been fed to the model themselves, but with rather more consistent results.

Also, the errors for these corrected variables will be adjusted according to their mathematical rules.

## Available constrains

1. "add_scalar":
	- $a+K=b$
	- base_variable = a
	- target_variable = b
	- constant = K
1. "mul_scalar":
	- $a*K=b$
	- base_variable = a
	- target_variable = b
	- constant = K
1. "const_sum":
	- $\sum W_i\cdot a_i=K$
	- variables = $[a_1, a_2, \cdots, a_n]$
	- reference_variable = $a_j$
	- constant_sum = K
	- weights = $[W_1, W_2, \cdots, W_n]$ or $W$ if $W_1=W_2= \cdots= W_n$ or fixed value $W$ if weights do not differ between columns
1. "custom_func":
	- to be used when none of the above is applicable and you have to develop your own functions to operate the dataframe
	- variables : list of the variables to be used
	- _validate\_function_: Function to assert if the received dataframe follows the given constrain.
	- _format\_function_: Write a string that describes the constrain equation.
	- _encode\_dataframe_: Create the new custom columns in the dataframe.
	- _decode\_dataframe_: Restore the original columns in the dataframe and calculate the propagated errors.


## Future additions

In the foreseeable future, some new constrains will be implemented, those are:

1. Variable sum
1. Constant and variable products
1. Conditionals

## Theoretical foundation

All of the worked out mathematics for the developed constrains can be found at the [calculations pdf](calculations.pdf)