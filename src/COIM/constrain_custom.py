from COIM.constrain import *

class Custom(Constrain):
	def __init__(self, variables, params, labels):
		super().__init__(variables, params, labels)
		self.validate_function, self.format_function, self.encode_function, self.decode_function=params
		self.labels=labels

	def validate_dataframe(self, df, cont):
		return self.validate_function(df, self.variables, self.labels)

	def format_rule(self):
		return self.format_function(self.variables, self.labels)

	def encode_dataframe(self, df):
		return self.encode_function(df, self.variables, self.labels)

	def decode_dataframe(self, df, errors):
		return self.decode_function(df, self.variables, self.labels, errors)
