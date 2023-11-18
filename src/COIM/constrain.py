class Constrain:
	def __init__(self, variables, params, labels=None):
		self.variables=variables
		self.params=params

	def validate_dataframe(self, df):
		return df

	def format_rule(self):
		return "Description"

	def encode_dataframe(self, df):
		return df

	def decode_dataframe(self, df, errors):
		return df, errors, del_vars
