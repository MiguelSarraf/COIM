from COIM.constrain import *

class ConstantSum(Constrain):
	def __init__(self, variables, reference_variable, constant_sum, weights=1, labels=None):
		"""
		(list, str, float, float/list, list)->None
		Save general parameters of the rule
		"""

		#Garantee parameters are consistent
		assert not labels or len(labels)==len(variables)-1, "Labels must correspond exactly to the last n-1 variables"
		assert isinstance(weights, (int, float)) or len(weights)==len(variables), "Weights must be a number or a list matching all the variables"

		#Initialize the supper class
		variables=variables
		params=constant_sum
		super().__init__(variables, params, labels)

		#Save appropriate parameters
		self.sum=constant_sum
		self.all_variables=variables[:]
		variables.remove(reference_variable)
		self.variables=variables
		self.A0=reference_variable
		self.weights=[weights for i in range(len(variables)+1)] if isinstance(weights, (int, float)) else weights
		self.labels={}
		if labels:
			for old, new in zip(self.variables, labels):
				self.labels[old]=new
		else:
			self.labels={old: old+"'" for old in self.variables}

	def validate_dataframe(self, df, cont):
		"""
		(DataFrame, int)->DataFrame
		Check if the rule is attended by the dataframe.
		Must return the complete dataframe.
		sum_{i=0}^N W_i * a_i = K
		"""
		df["sum"]=0
		for weight, var in zip(self.weights, self.all_variables):
			assert var in df, f"Variable {var} not in dataframe"
			df["sum"]+=df[var]*weight #sum_{i=0}^N W_i * a_i
			df["diff"]=abs(df["sum"]-self.sum) #sum_{i=0}^N W_i * a_i - K
		
		#Check if rule conforms
		df_filter=df[df["diff"]>self.precision]
		if len(df_filter)!=0:
			print(self.sum)
			raise ValueError(f"The following lines does not conform to rule {cont}\n{df_filter}")

		#Remove unnecessary columns
		df=df.drop("sum", axis=1)
		df=df.drop("diff", axis=1)
		return df

	def format_rule(self):
		"""
		(None)->str
		Returns a string describing the rule.
		"""
		rule=""
		for weight, var in zip(self.weights, self.all_variables):
			if weight==1:
				rule+="{}+".format(var)
			else:
				rule+="{}*{}+".format(weight, var)
		return rule[:-1]+"={}".format(self.sum)

	def encode_dataframe(self, df):
		"""
		(DataFrame)->DataFrame
		Apply the developed formulas to reduce the dataframe columns.
		a_i'=\frac{a_i}{a_0 K}
		"""
		for var in self.variables:
			df[self.labels[var]]=df[var]/(self.sum*df[self.A0])
		df.drop(columns=self.variables+[self.A0], inplace=True)
		return df

	def decode_dataframe(self, df, errors):
		"""
		(DataFrame, DataFrame)->DataFrame, DataFrame
		Apply the reverse formulas to restore the original columns
		and propagate the errors.
		"""

		#Calculate sums
		df["sum"]=0
		errors["sum"]=0
		for weight, var in zip(self.weights[1:], self.variables):
			df["sum"]+=df[self.labels[var]]*weight #sum_{i=1}^N W_i * a_i
			errors["sum"]+=errors[self.labels[var]]**2*weight**2 #sum_{j=1}^NW_j^2*Delta a_j'^2

		#Retrieve variables
		"""a_0={K}/{W_0+K*sum_{i=1}^N W_i * a_i'}"""
		df[self.A0]=self.sum/(self.weights[0]+self.sum*df["sum"])
		"""a_i=a_i'a_0K"""
		for var in self.variables:
			df[var]=df[self.labels[var]]*df[self.A0]*self.sum

		#Propagate errors
		means=df.aggregate("mean")
		"""Delta a_0=a_0^2*sqrt{sum_{j=1}^NW_j^2*Delta a_j'^2}"""
		errors[self.A0]=(means[self.A0]**2)*(errors["sum"]**.5)
		"""Delta a_i=|(K-W_i*a_i)/(a_0W_i)|*sqrt{a_0^4W_i^2*Delta a_i'^2+Delta a_0^2}'"""
		for weight, var in zip(self.weights[1:], self.variables):
			factor=(self.sum-weight*means[var])/(means[self.A0]*weight)
			error_sum=means[self.A0]**4*weight**2*errors[self.labels[var]]**2+errors[self.A0]**2
			errors[var]=abs(factor)*error_sum**.5

		#Remove unnecessary columns
		df.drop(columns=[self.labels[var] for var in self.variables]+["sum"], inplace=True)
		errors.drop(columns=[self.labels[var] for var in self.variables]+["sum"], inplace=True)
		return df, errors
