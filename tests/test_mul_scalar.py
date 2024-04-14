import pandas as pd
import sys
sys.path.insert(1,'../src')
from COIM.operator import ConstrainOperator, MulScalar
import numpy as np
import logging as lg

lg.getLogger().setLevel(lg.DEBUG)

def test_mul_scalar(verbose=False):
	lg.info("test_constant_sum tests a 100 rows, 2 columns DataFrame where b=10*a")
	df=np.random.uniform(low=0, high=10, size=(1,100)).astype("int")
	df=pd.DataFrame(df.T, columns=["a"])
	df["b"]=df["a"]*10
	if verbose:
		print("Orginal dataset")
		print(df.head())

	CO=ConstrainOperator()
	MS=MulScalar(base_variable="a", target_variable="b", constant=10, labels=["new_a"])
	CO.add_rule(MS)

	new_df=CO.encode_dataframe(df)
	if verbose:
		print("Encoded dataset")
		print(new_df.head())

	errors=pd.DataFrame([[0.0005]], columns=["new_a"])
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

	diff=df.compare(new_df)
	if len(diff)>0:
		lg.error("Decoded DataFrame does not match original one.")
		lg.debug(diff.head())

	assert len(diff)==0

if __name__=="__main__":
	test_mul_scalar(True)