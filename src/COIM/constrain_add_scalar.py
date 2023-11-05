from COIM.constrain import *

class AddScalar(Constrain):
	def __init__(self, variables, params, labels):
		assert not labels, "Labels not needed for add_scalar"
		assert len(variables)==2, "There must be exactly two variables, a and b"
		assert len(params)==1, "There must be exactly one param, the scalar"
		super().__init__(variables, params, labels)
		self.K=self.params[0]
		self.A, self.B=variables

	def validate_dataframe(self, df, cont):
		df_filter=df[df[self.B]!=df[self.A]+self.K]
		if len(df_filter)!=0:
			raise ValueError(f"The following lines does not conform to rule {cont}\n{df_filter}")
		return df

	def format_rule(self):
		return f"{self.A}+{self.K}={self.B}"

	def encode_dataframe(self, df):
		return df, {self.B}

	def decode_dataframe(self, df, errors):
		df[self.B]=df[self.A]+self.K
		errors[self.B]=errors[self.A]
		return df, errors, {}
