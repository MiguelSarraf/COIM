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

	def add_rule(self, operation, variables, params=None, index=None, labels=None):
		assert operation in self.valid_ops, "Invalid operation"
		rule=self.valid_ops[operation](variables, params, labels)
		if index:
			assert isinstance(index, int) and index>=0 and index<len(self.operations), "Index is not valid"
			self.operations=self.operations[:index]+[rule]+self.operations[index:]
		else:
			self.operations.append(rule)

	def show_rules(self):
		cont=0
		for operation in self.operations:
			print("{:5s} {:50s}".format(str(cont), operation.format_rule()))
			cont+=1

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
			df, remove=rule.encode_dataframe(df)
			removed_cols=removed_cols.union(remove)
		df=df.drop(removed_cols, axis=1)
		return df

	def decode_dataframe(self, df, errors):
		removed_cols=set()
		for rule in self.operations:
			df, errors, remove=rule.decode_dataframe(df, errors)
			removed_cols=removed_cols.union(remove)
		df=df.drop(removed_cols, axis=1)
		errors=errors.drop(removed_cols, axis=1)
		return df, errors
