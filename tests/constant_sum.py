import pandas as pd
import sys
sys.path.insert(1,'../src')
from COIM.operator import ConstrainOperator
import numpy as np

df=np.random.uniform(low=25, high=38, size=(2,100)).astype("int")

df=pd.DataFrame(df.T, columns=["a0", "a1"])
df["a2"]=100-df["a0"]-df["a1"]
print("Orginal dataset")
print(df)

CO=ConstrainOperator()

CO.add_rule("const_sum", ["a0", "a1", "a2"], [100], labels=["new_a1", "new_a2"])
print("Applied rules")
CO.show_rules()
new_df=CO.encode_dataframe(df)
print("Encoded dataset")
print(new_df)
errors=pd.DataFrame([[0.005,0.003]], columns=["new_a1", "new_a2"])
print("Errors")
print(errors)
new_df, errors=CO.decode_dataframe(new_df, errors)
print("Decoded dataset")
print(new_df)
print("Decoded errors")
print(errors)
