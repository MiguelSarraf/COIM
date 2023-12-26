import pandas as pd
import sys
sys.path.insert(1,'../src')
from COIM.operator import ConstrainOperator, MulScalar, ConstantSum
import numpy as np

df=np.random.uniform(low=2.5, high=3.8, size=(2,100))
df=pd.DataFrame(df.T, columns=["a0", "a1"])
df["a2"]=(10-df["a0"]-df["a1"])
df["a0pctg"]=df.a0*.1
df["a1pctg"]=df.a1*.1
df["a2pctg"]=df.a2*.1
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

df=CO.encode_dataframe(df)
print("Encoded dataset")
print(df.head())

errors=pd.DataFrame([[0.0005,0.0003]], columns=["new_a1", "new_a2"])
print("Errors")
print(errors.head())

df, errors=CO.decode_dataframe(df, errors)
print("Decoded dataset")
print(df.head())
print("Decoded errors")
print(errors.head())

CO.summary()