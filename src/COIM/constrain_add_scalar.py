from COIM.constrain import *

class AddScalar(Constrain):
	def __init__(self, base_variable, target_variable, constant, labels=None):
		assert not labels, "Labels not needed for add_scalar"
		variables=[base_variable, target_variable]
		params=[constant]
		super().__init__(variables, params, labels)
		self.K=constant
		self.A=base_variable
		self.B=target_variable

	def validate_dataframe(self, df, cont):
		df_filter=df[df[self.B]!=df[self.A]+self.K]
		if len(df_filter)!=0:
			raise ValueError(f"The following lines does not conform to rule {cont}\n{df_filter}")
		return df

	def format_rule(self):
		return f"{self.A}+{self.K}={self.B}"

	def encode_dataframe(self, df):
		df.drop(columns=self.B, inplace=True)
		return df

	def decode_dataframe(self, df, errors):
		df[self.B]=df[self.A]+self.K
		errors[self.B]=errors[self.A]
		return df, errors
