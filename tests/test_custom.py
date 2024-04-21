import pandas as pd
import sys
import os
sys.path.insert(1,'../src')
from COIM.operator import ConstrainOperator, Custom
import numpy as np
import logging as lg

lg.getLogger().setLevel(lg.DEBUG)
k=3

def vali(df, vars, labels):
	df[labels[0]]=k*df[vars[0]]
	df_filter=df[df["nk"]!=df["kn"]]
	assert len(df_filter)==0, "Does not conform to rule"
	df.drop(columns=labels[0], inplace=True)
	return df

def form(vars, labels):
	return f"{labels[0]}={k}*{vars[0]}"

def enco(df, vars, labels):
	df.drop(columns=list([vars[1]]), inplace=True)
	return df

def deco(df, vars, labels, errors):
	df[labels[0]]=k*df[vars[0]]
	errors[labels[0]]=k*errors[vars[0]]
	return df, errors

def test_custom(verbose=False):
	precision=os.environ.get("PRECISION", 10)
	lg.info(f"test_custom tests a 100 rows, 2 columns DataFrame where nk={k}*n")
	df=np.random.uniform(low=0, high=10, size=(1,100)).astype("int")
	df=pd.DataFrame(df.T, columns=["n"])
	df["nk"]=k*df["n"]
	if verbose:
		print("Orginal dataset")
		print(df.head())

	CO=ConstrainOperator()
	CUST=Custom(["n", "nk"], vali, form, enco, deco, labels=["kn"])
	CO.add_rule(CUST)

	new_df=CO.encode_dataframe(df)
	if verbose:
		print("Encoded dataset")
		print(new_df.head())

	errors=pd.DataFrame([[0.01]], columns=["n"])
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

	new_df.rename(columns={"kn":"nk"}, inplace=True)

	diff=df.compare(new_df)
	if len(diff)>0:
		lg.error("Decoded DataFrame does not match original one.")
		lg.debug(diff.head())

	assert len(diff)==0

if __name__=="__main__":
	test_custom(True)
