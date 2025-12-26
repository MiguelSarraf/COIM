class Constrain:
	"""
	General class to store the rules.
	"""
	def __init__(self, variables, params, labels=None, precision=1e-10):
		"""
		(list, list, list, float)->None
		Save general parameters of the rule
		"""
		self.variables=variables
		self.params=params
		self.precision=precision

	def validate_dataframe(self, df):
		"""
		(DataFrame)->DataFrame
		Check if the rule is attended by the dataframe.
		Must return the complete dataframe.
		"""
		return df

	def format_rule(self):
		"""
		(None)->str
		Returns a string describing the rule.
		"""
		return "Description"

	def encode_dataframe(self, df):
		"""
		(DataFrame)->DataFrame
		Apply the developed formulas to reduce the dataframe columns.
		"""
		return df

	def decode_dataframe(self, df, errors):
		"""
		(DataFrame, DataFrame)->DataFrame, DataFrame
		Apply the reverse formulas to restore the original columns
		and propagate the errors.
		"""
		return df, errors
