import pandas as pd
import sys
import os
sys.path.insert(1,'../src')
from COIM.operator import ConstrainOperator, ConstantSum
import numpy as np
import logging as lg

lg.getLogger().setLevel(lg.DEBUG)

def test_constant_sum(verbose=False):
	precision=os.environ.get("PRECISION", 10)
	lg.info("test_constant_sum tests a 100 rows, 3 columns DataFrame where a0+a1+2*a2=10")
	df=np.random.uniform(low=2.5, high=3.8, size=(2,100))
	df=pd.DataFrame(df.T, columns=["a0", "a1"])
	df["a2"]=(10-df["a0"]-df["a1"])/2
	if verbose:
		print("Orginal dataset")
		print(df.head())

	CO=ConstrainOperator()
	CS=ConstantSum(variables=["a0", "a1", "a2"], reference_variable="a0", constant_sum=10, weights=[1,1,2], labels=["new_a1", "new_a2"])
	CO.add_rule(CS)

	new_df=CO.encode_dataframe(df)
	if verbose:
		print("Encoded dataset")
		print(new_df.head())

	errors=pd.DataFrame([[0.0005,0.0003]], columns=["new_a1", "new_a2"])
	if verbose:
		print("Errors")
		print(errors.head())

	new_df, errors=CO.decode_dataframe(new_df, errors)
	if verbose:
		print("Decoded dataset")
		print(new_df.head())
		print("Decoded errors")
		print(errors.head())

	if verbose:
		CO.summary()

	df=df.round(precision)
	new_df=new_df.round(precision)

	diff=df.compare(new_df)
	if len(diff)>0:
		lg.error("Decoded DataFrame does not match original one.")
		lg.debug(diff.head())

	assert len(diff)==0

if __name__=="__main__":
	test_constant_sum(True)
