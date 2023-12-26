from COIM.constrain import *

class MulScalar(Constrain):
	def __init__(self, base_variable, target_variable, constant, labels=None):
		"""
		(str, str, float, list)->None
		Save general parameters of the rule
		"""

		#Garantee parameters are consistent
		assert not labels or len(labels)==1, "Labels must correspond exactly to the second variables"

		#Initialize the supper class
		variables=[base_variable, target_variable]
		params=[constant]
		super().__init__(variables, params, labels)

		#Save appropriate parameters
		self.K=constant
		self.A=base_variable
		self.B=target_variable
		self.labels={self.A: "new_"+self.A if not labels else labels[0]}

	def validate_dataframe(self, df, cont):
		"""
		(DataFrame)->DataFrame
		Check if the rule is attended by the dataframe.
		Must return the complete dataframe.
		"""
		
		#Check if rule conforms
		df_filter=df[abs(df[self.B]-df[self.A]*self.K)>self.precision]#b-a*K
		if len(df_filter)!=0:
			raise ValueError(f"The following lines does not conform to rule {cont}\n{df_filter}")
		return df

	def format_rule(self):
		"""
		(None)->str
		Returns a string describing the rule.
		"""
		return f"{self.A}*{self.K}={self.B}"

	def encode_dataframe(self, df):
		"""
		(DataFrame)->DataFrame
		Apply the developed formulas to reduce the dataframe columns.
		a'=a if |K|>1 else b
		"""
		if abs(self.K)<=1:
			df[self.labels[self.A]]=df[self.B]
		else:
			df[self.labels[self.A]]=df[self.A]
		df.drop(columns=[self.A, self.B], inplace=True)
		return df

	def decode_dataframe(self, df, errors):
		"""
		(DataFrame, DataFrame)->DataFrame, DataFrame
		Apply the reverse formulas to restore the original columns
		and propagate the errors.
		"""
		if abs(self.K)<=1:
			df.rename(columns={self.labels[self.A]:self.B}, inplace=True)
			df[self.A]=df[self.B]/self.K
			errors.rename(columns={self.labels[self.A]:self.B}, inplace=True)
			errors[self.A]=errors[self.B]/self.K
		else:
			df.rename(columns={self.labels[self.A]:self.A}, inplace=True)
			df[self.B]=df[self.A]*self.K
			errors.rename(columns={self.labels[self.A]:self.A}, inplace=True)
			errors[self.B]=errors[self.A]*self.K
		return df, errors
