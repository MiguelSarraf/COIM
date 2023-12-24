from prettytable import PrettyTable
from COIM.constrain_custom import *
from COIM.constrain_constant_sum import *
from COIM.constrain_add_scalar import *
from COIM.constrain_mul_scalar import *

class ConstrainOperator:
	def __init__(self, name="COIM", print_width=30):
		self.name=name
		self.operations=[]
		self.print_width=print_width
		self._encoded=False
		self._decoded=False

	def add_rule(self, rule, index=None):
		if index:
			assert isinstance(index, int) and index>=0 and index<len(self.operations), "Index is not valid"
			self.operations=self.operations[:index]+[rule]+self.operations[index:]
		else:
			self.operations.append(rule)

	def show_rules(self, table=None):
		if not table: table=PrettyTable()
		table.title=f"{self.name} rules"
		table.field_names=["Position", "Constrain"]
		table.min_width=self.print_width
		rules_list=[[i, op.format_rule()] for i, op in zip(range(1, len(self.operations)+1), self.operations)]
		table.add_rows(rules_list)
		return table

	def show_encode(self, table=None):
		if not self._encoded: return
		if not table: table=PrettyTable()
		table.title=f"{self.name} encode results"
		table.field_names=["Variable", "Value"]
		table.min_width=self.print_width
		table.add_row(["Variation reduction", f"{round(100*(self._variance_gain), 3)} %"])
		table.add_row(["Columns reduction", f"{round(100*(self._col_gain), 3)} %"])
		return table

	def show_decode(self, table=None):
		if not self._decoded: return
		if not table: table=PrettyTable()
		table.title=f"{self.name} decode results"
		table.field_names=["Variable", "Value"]
		table.min_width=self.print_width
		table.add_row(["Error/mean value reduction", f"{round(100*(self._error_value_gain), 3)} %"])
		return table

	def summary(self):
		t_rules=str(self.show_rules())
		t_encode=str(self.show_encode())
		t_decode=str(self.show_decode())
		size=t_encode.index("\n")
		print(t_rules+t_encode[size:]+t_decode[size:])

	def validate_dataframe(self, df):
		cont=0
		for rule in self.operations:
			df=rule.validate_dataframe(df, cont)
			cont+=1
		return df

	def encode_dataframe(self, df):
		df=self.validate_dataframe(df)
		self._encoded=True
		previous_variance=df.var().sum()
		previous_cols=len(df.columns)
		for rule in self.operations:
			df=rule.encode_dataframe(df)
		later_variance=df.var().sum()
		later_cols=len(df.columns)
		self._variance_gain=1-later_variance/previous_variance
		self._col_gain=1-later_cols/previous_cols
		return df

	def decode_dataframe(self, df, errors):
		self._decoded=True
		previous_error=(errors/df.mean()).mean().mean()
		for rule in self.operations[::-1]:
			df, errors=rule.decode_dataframe(df, errors)
		later_error=(errors/df.mean()).mean().mean()
		self._error_value_gain=1-later_error/previous_error
		return df, errors
