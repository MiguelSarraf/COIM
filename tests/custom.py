import pandas as pd
import sys
sys.path.insert(1,'../src')
from COIM.operator import ConstrainOperator, Custom
import numpy as np

df=np.random.uniform(low=0, high=10, size=(1,100)).astype("int")

k=3
df=pd.DataFrame(df.T, columns=["n"])
df["nk"]=k*df["n"]
print("Orginal dataset")
print(df.head())

def vali(df, vars, labels):
	df[labels[0]]=k*df[vars[0]]
	df_filter=df[df["nk"]!=df["kn"]]
	assert len(df_filter)==0, "Does not conform to rule"
	df=df.drop(labels[0], axis=1)
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

CO=ConstrainOperator()
CUST=Custom(["n", "nk"], [vali, form, enco, deco], labels=["kn"])

CO.add_rule(CUST)
print("Applied rules")
CO.show_rules()
new_df=CO.encode_dataframe(df)
print("Encoded dataset")
print(new_df.head())
errors=pd.DataFrame([[0.01]], columns=["n"])
print("Errors")
print(errors.head())
new_df, errors=CO.decode_dataframe(new_df, errors)
print("Decoded dataset")
print(new_df.head())
print("Decoded errors")
print(errors.head())
