from COIM.constrain import *

class AddScalar(Constrain):
	def __init__(self, variables, params, labels):
		assert not labels or len(labels)==1, "Labels must correspond exactly to the second variables"
		assert len(variables)==2, "There must be exactly two variables, a and b"
		assert len(params)==1, "There must be exactly one param, the scalar"
		super().__init__(variables, params, labels)
		self.K=self.params[0]
		self.A, self.B=variables
		self.labels={self.A: "new_"+self.A if not labels else labels[0]}

	def validate_dataframe(self, df, cont):
		df_filter=df[df[self.B]!=df[self.A]+self.K]
		if len(df_filter)!=0:
			raise ValueError(f"The following lines does not conform to rule {cont}\n{df_filter}")
		return df

	def format_rule(self):
		return f"{self.A}+{self.K}={self.B}"

	def encode_dataframe(self, df):
		df[self.labels[self.A]]=df[self.A]
		return df, {self.A, self.B}

	def decode_dataframe(self, df, errors):
		df.rename(columns={self.labels[self.A]:self.A}, inplace=True)
		df[self.B]=df[self.A]+self.K
		errors.rename(columns={self.labels[self.A]:self.A}, inplace=True)
		errors[self.B]=errors[self.A]
		return df, errors, {}
