import pandas as pd
import sys
sys.path.insert(1,'../src')
from COIM.operator import ConstrainOperator, ConstantSum
import numpy as np

df=np.random.uniform(low=2.5, high=3.8, size=(2,100))
df=pd.DataFrame(df.T, columns=["a0", "a1"])
df["a2"]=10-df["a0"]-df["a1"]
print("Orginal dataset")
print(df.head())

CO=ConstrainOperator()
CS=ConstantSum(variables=["a1", "a2"], reference_variable="a0", constant_sum=10, labels=["new_a1", "new_a2"])
CO.add_rule(CS)

new_df=CO.encode_dataframe(df)
print("Encoded dataset")
print(new_df.head())

errors=pd.DataFrame([[0.0005,0.0003]], columns=["new_a1", "new_a2"])
print("Errors")
print(errors.head())

new_df, errors=CO.decode_dataframe(new_df, errors)
print("Decoded dataset")
print(new_df.head())
print("Decoded errors")
print(errors.head())

CO.summary()
