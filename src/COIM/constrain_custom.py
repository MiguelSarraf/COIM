from COIM.constrain import *

class Custom(Constrain):
	def __init__(self, variables, validate_function, format_function, encode_function, decode_function, labels=None, precision=1e-10):
		"""
		(list, list, list, float)->None
		Save general parameters of the rule
		"""

		#Initialize the supper class
		params=validate_function, format_function, encode_function, decode_function
		super().__init__(variables, params, labels, precision)

		#Save appropriate parameters
		self.validate_function=validate_function
		self.format_function=format_function
		self.encode_function=encode_function
		self.decode_function=decode_function
		self.labels=labels

	def validate_dataframe(self, df, cont):
		"""
		(DataFrame)->DataFrame
		Check if the rule is attended by the dataframe.
		Must return the complete dataframe.
		"""
		df=df.copy()
		return self.validate_function(df, self.variables, self.labels)

	def format_rule(self):
		"""
		(None)->str
		Returns a string describing the rule.
		"""
		return self.format_function(self.variables, self.labels)

	def encode_dataframe(self, df):
		"""
		(DataFrame)->DataFrame
		Apply the developed formulas to reduce the dataframe columns.
		"""
		df=df.copy()
		return self.encode_function(df, self.variables, self.labels)

	def decode_dataframe(self, df, errors):
		"""
		(DataFrame, DataFrame)->DataFrame, DataFrame
		Apply the reverse formulas to restore the original columns
		and propagate the errors.
		"""
		df=df.copy()
		errors=errors.copy()
		return self.decode_function(df, self.variables, self.labels, errors)
