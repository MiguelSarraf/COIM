from tabulate import tabulate
from COIM.constrain_custom import *
from COIM.constrain_constant_sum import *
from COIM.constrain_add_scalar import *
from COIM.constrain_mul_scalar import *

class ConstrainOperator:
	def __init__(self, name="COIM"):
		self.name=name
		self.operations=[]
		self.valid_ops={"custom_func": 	Custom,
						"const_sum": 	ConstantSum,
						"add_scalar":	AddScalar,
						"mul_scalar":	MulScalar}

	def add_rule(self, rule, index=None):
		if index:
			assert isinstance(index, int) and index>=0 and index<len(self.operations), "Index is not valid"
			self.operations=self.operations[:index]+[rule]+self.operations[index:]
		else:
			self.operations.append(rule)

	def show_rules(self):
		rules_list=[[i, op.format_rule()] for i, op in zip(range(1, len(self.operations)+1), self.operations)]
		print(tabulate(rules_list, headers=["position", "constrian"], tablefmt="rst"))

	def validate_dataframe(self, df):
		cont=0
		for rule in self.operations:
			df=rule.validate_dataframe(df, cont)
			cont+=1
		return df

	def encode_dataframe(self, df):
		df=self.validate_dataframe(df)
		removed_cols=set()
		for rule in self.operations:
			df=rule.encode_dataframe(df)
		return df

	def decode_dataframe(self, df, errors):
		removed_cols=set()
		for rule in self.operations[::-1]:
			df, errors=rule.decode_dataframe(df, errors)
		return df, errors
