from COIM.constrain import *

class Custom(Constrain):
	def __init__(self, variables, validate_function, format_function, encode_function, decode_function, labels=None):
		params=validate_function, format_function, encode_function, decode_function
		super().__init__(variables, params, labels)
		self.validate_function=validate_function
		self.format_function=format_function
		self.encode_function=encode_function
		self.decode_function=decode_function
		self.labels=labels

	def validate_dataframe(self, df, cont):
		return self.validate_function(df, self.variables, self.labels)

	def format_rule(self):
		return self.format_function(self.variables, self.labels)

	def encode_dataframe(self, df):
		return self.encode_function(df, self.variables, self.labels)

	def decode_dataframe(self, df, errors):
		return self.decode_function(df, self.variables, self.labels, errors)
