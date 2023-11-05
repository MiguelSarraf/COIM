# COIM

Constrain Operator for Inferential Models is a simple tool for pre and pos processing of data to eliminate redunduncy in datasets caused by dependency rules between the variables/columns.

## Usage

To start using COIM, import into your code the operator class, which orquestrates the constrains and define an instance.

```
from COIM.operator import ConstrainOperator
CO=ConstrainOperator()
```

To add a new constrain, use the _add\_rule_ method from ConstrainOperator class.

```CO.add_rule(operation, variables, params, index, labels)```

 - _operation_: Especifies the constrain to be applied (str)
 - _variables_: The columns names of the variables used in the constrain (list[str])
 - _params_: The columns names of the other parameters used in the constrain (list[str])
 - _index_: The position to be occupied by the constrain in the constrains sequence (int). Optional
 - _labels_: The names to be assigned to the generated new columns (list[str]). Optional

Then you can encode your dataframe to use the new corrected variables to feed your model.

```new_df=CO.encode_dataframe(df)```

After running your model, you can regenerate the data in the original format, decoding the acquired values and errors.

```decoded_df, decoded_errors=CO.decode_dataframe(predicted_df, errors)```

That will yield the predictions for the original variables as if they had been fed to the model themselves, but with rather more consistent results

## Available constrains

1. "add_scalar":
	- $a+K=b$
	- _variables_=[a, b]
 	- _params_=[K]
1. "const_sum":
	- $\sum a_i=K$
	- _variables_=[ $a_1$, $a_2$, $\cdots$, $a_n$]
 	- _params_=[K]
1. "custom_func":
	- to be used when none of the above is applicable
	- you have to develop your own functions to operate the dataframe
		1. _validate\_function_: Function to assert if the received dataframe follows the given constrain. (df[DataFrame], variables[list], labels[list])->bool
		1. _format\_function_: Write a string that describes the constrain equation. (variables[list], labels[list])->str
		1. _encode\_dataframe_: Create the new custom columns in the dataframe. (df[DataFrame], variables[list], labels[list])->DataFrame
		1. _decode\_dataframe_: Restore the original columns in the dataframe and calculate the propagated errors. (df[DataFrame], variables[list], labels[list], errors[DataFrame])->DataFrame, DataFrame
	- _params_=[_validate\_function_, _format\_function_, _encode\_dataframe_, _decode\_dataframe_]


## Future additions

In the foreseeable future, some new constrains will be implemented, those are:

1. Multiplication by scalar
1. Variable sum
1. Conditionals

## Theoretical foundation

All of the worked out mathematics for the developed constrains can be found at the [calculations pdf](calculations.pdf)