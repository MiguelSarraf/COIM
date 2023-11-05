import pandas as pd
import sys
sys.path.insert(1,'../src')
from COIM.operator import ConstrainOperator
import numpy as np

df=np.random.uniform(low=0, high=10, size=(1,100)).astype("int")

df=pd.DataFrame(df.T, columns=["a"])
df["b"]=df["a"]+10
print("Orginal dataset")
print(df)

CO=ConstrainOperator()

CO.add_rule("add_scalar", ["a", "b"], [10])
print("Applied rules")
CO.show_rules()
new_df=CO.encode_dataframe(df)
print("Encoded dataset")
print(new_df)
errors=pd.DataFrame([[0.0005]], columns=["a"])
print("Errors")
print(errors)
new_df, errors=CO.decode_dataframe(new_df, errors)
print("Decoded dataset")
print(new_df)
print("Decoded errors")
print(errors)
