import pandas as pd
import sys
import os
sys.path.insert(1,'../src')
from COIM.operator import ConstrainOperator, MulScalar, ConstantSum
import numpy as np
import logging as lg

lg.getLogger().setLevel(lg.DEBUG)

def test_multi_constrain(verbose=False):
	precision=os.environ.get("PRECISION", 10)
	lg.info("test_constant_sum tests a 100 rows, 2 columns DataFrame where a0+a1+a2=10 and anpctg=an*0.1")
	df=np.random.uniform(low=2.5, high=3.8, size=(2,100))
	df=pd.DataFrame(df.T, columns=["a0", "a1"])
	df["a2"]=(10-df["a0"]-df["a1"])
	df["a0pctg"]=df.a0*.1
	df["a1pctg"]=df.a1*.1
	df["a2pctg"]=df.a2*.1
	if verbose:
		print("Orginal dataset")
		print(df.head())

	CO=ConstrainOperator()
	MS0=MulScalar(base_variable="a0", target_variable="a0pctg", constant=.1, labels=["a0pc"])
	MS1=MulScalar(base_variable="a1", target_variable="a1pctg", constant=.1, labels=["a1pc"])
	MS2=MulScalar(base_variable="a2", target_variable="a2pctg", constant=.1, labels=["a2pc"])
	CO.add_rule(MS0)
	CO.add_rule(MS1)
	CO.add_rule(MS2)
	CS=ConstantSum(variables=["a0pc", "a1pc", "a2pc"], reference_variable="a0pc", constant_sum=1, labels=["new_a1", "new_a2"])
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

	diff=new_df.compare(new_df)
	if len(diff)>0:
		lg.error("Decoded DataFrame does not match original one.")
		lg.debug(diff.head())

	assert len(diff)==0

if __name__=="__main__":
	test_multi_constrain(True)