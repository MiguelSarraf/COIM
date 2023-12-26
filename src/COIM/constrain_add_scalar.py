from COIM.constrain import *

class AddScalar(Constrain):
	def __init__(self, base_variable, target_variable, constant, labels=None):
		"""
		(list, list, list, float)->None
		Save general parameters of the rule
		"""

		#Garantee parameters are consistent
		assert not labels, "Labels not needed for add_scalar"

		#Initialize the supper class
		variables=[base_variable, target_variable]
		params=[constant]
		super().__init__(variables, params, labels)

		#Save appropriate parameters
		self.K=constant
		self.A=base_variable
		self.B=target_variable

	def validate_dataframe(self, df, cont):
		"""
		(DataFrame)->DataFrame
		Check if the rule is attended by the dataframe.
		Must return the complete dataframe.
		"""
		
		#Check if rule conforms
		df_filter=df[abs(df[self.B]-(df[self.A]+self.K))>self.precision]# b-(a+K)
		if len(df_filter)!=0:
			raise ValueError(f"The following lines does not conform to rule {cont}\n{df_filter}")
		return df

	def format_rule(self):
		"""
		(None)->str
		Returns a string describing the rule.
		"""
		return f"{self.A}+{self.K}={self.B}"

	def encode_dataframe(self, df):
		"""
		(DataFrame)->DataFrame
		Apply the developed formulas to reduce the dataframe columns.
		"""
		df.drop(columns=self.B, inplace=True)
		return df

	def decode_dataframe(self, df, errors):
		"""
		(DataFrame, DataFrame)->DataFrame, DataFrame
		Apply the reverse formulas to restore the original columns
		and propagate the errors.
		"""
		df[self.B]=df[self.A]+self.K
		errors[self.B]=errors[self.A]
		return df, errors
