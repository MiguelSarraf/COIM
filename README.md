# COIM

Constrain Operator for Inferential Models is a simple tool for pre and pos processing of data to eliminate redunduncy in datasets caused by dependency rules between the variables/columns.

## Usage

To start using COIM, import into your code the operator class, which orquestrates the constrains and define an instance.

```
from COIM import ConstrainOperator
CO=ConstrainOperator()
```

To add a new constrain, use the _add\_rule_ method from ConstrainOperator class.

```
from COIM import SomeConstrain
SC=SomeConstrain(**parameters)
CO.add_rule(SC)
```

Each constrain will require their own specific parameters, refer to section _Available constrains_ to know each of them. However, all constrains receive the parameter "labels", which is a list with the new names to be used on the encoded columns.

Then you can encode your dataframe to use the new corrected variables to feed your model.

```new_df=CO.encode_dataframe(df)```

After running your model, you can regenerate the data in the original format, decoding the acquired values and errors.

```decoded_df, decoded_errors=CO.decode_dataframe(predicted_df, errors)```

That will yield the predictions for the original variables as if they had been fed to the model themselves, but with rather more consistent results

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
	- weights = $[W_1, W_2, \cdots, W_n]$ or $W$ if $W_1=W_2= \cdots= W_n$
1. "custom_func":
	- to be used when none of the above is applicable and you have to develop your own functions to operate the dataframe
	- variables : list of the variables to be used
	- _validate\_function_: Function to assert if the received dataframe follows the given constrain. (df[DataFrame], variables[list], labels[list])->bool
	- _format\_function_: Write a string that describes the constrain equation. (variables[list], labels[list])->str
	- _encode\_dataframe_: Create the new custom columns in the dataframe. (df[DataFrame], variables[list], labels[list])->DataFrame
	- _decode\_dataframe_: Restore the original columns in the dataframe and calculate the propagated errors. (df[DataFrame], variables[list], labels[list], errors[DataFrame])->DataFrame, DataFrame


## Future additions

In the foreseeable future, some new constrains will be implemented, those are:

1. Variable sum
1. Constant and variable products
1. Conditionals

## Theoretical foundation

All of the worked out mathematics for the developed constrains can be found at the [calculations pdf](calculations.pdf)