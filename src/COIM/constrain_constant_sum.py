from COIM.constrain import *

class ConstantSum(Constrain):
	def __init__(self, variables, params, labels):
		assert not labels or len(labels)==len(variables)-1, "Labels must correspond exactly to the last n-1 variables"
		super().__init__(variables, params, labels)
		self.sum=self.params[0]
		self.variables=variables[1:]
		self.A0=variables[0]
		self.labels={}
		if labels:
			for old, new in zip(self.variables, labels):
				self.labels[old]=new
		else:
			self.labels={old: old+"'" for old in self.variables}

	def validate_dataframe(self, df, cont):
		df["sum"]=0
		for var in self.variables+[self.A0]:
			assert var in df, f"Variable {var} not in dataframe"
			df["sum"]+=df[var]
		df_filter=df[df["sum"]!=self.sum]
		if len(df_filter)!=0:
			raise ValueError(f"The following lines does not conform to rule {cont}\n{df_filter}")
		df=df.drop("sum", axis=1)
		return df

	def format_rule(self):
		return f"{'+'.join([self.A0]+self.variables)}={self.sum}"

	def encode_dataframe(self, df):
		for var in self.variables:
			df[self.labels[var]]=df[var]/(self.sum*df[self.A0])
		return df, set(self.variables+[self.A0])

	def decode_dataframe(self, df, errors):
		df["sum"]=0
		errors["sum"]=0
		for var in self.variables:
			df["sum"]+=df[self.labels[var]]
			errors["sum"]+=errors[self.labels[var]]**2
		df[self.A0]=self.sum/(1+self.sum*df["sum"])
		for var in self.variables:
			df[var]=df[self.labels[var]]*df[self.A0]*self.sum
		means=df.aggregate("mean")
		errors[self.A0]=(means[self.A0]**2)*(errors["sum"]**.5)
		for var in self.variables:
			errors[var]=means[self.A0]*(self.sum-means[var])*errors[self.labels[var]]
		return df, errors, [self.labels[var] for var in self.variables]+["sum"]
