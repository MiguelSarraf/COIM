import pandas as pd
import sys
sys.path.insert(1,'../src')
from COIM.operator import ConstrainOperator, MulScalar
import numpy as np

def test_mul_scalar():
	df=np.random.uniform(low=0, high=10, size=(1,100)).astype("int")
	df=pd.DataFrame(df.T, columns=["a"])
	df["b"]=df["a"]*10
	print("Orginal dataset")
	print(df.head())

	CO=ConstrainOperator()
	MS=MulScalar(base_variable="a", target_variable="b", constant=10, labels=["new_a"])
	CO.add_rule(MS)

	new_df=CO.encode_dataframe(df)
	print("Encoded dataset")
	print(new_df.head())

	errors=pd.DataFrame([[0.0005]], columns=["new_a"])
	print("Errors")
	print(errors.head())

	new_df, errors=CO.decode_dataframe(new_df, errors)
	print("Decoded dataset")
	print(new_df.head())
	print("Decoded errors")
	print(errors.head())

	CO.summary()

	assert len(df.compare(new_df))==0

if __name__=="__main__":
	test_mul_scalar()