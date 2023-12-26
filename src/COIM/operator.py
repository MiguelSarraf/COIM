from prettytable import PrettyTable
import pickle
from COIM.constrain_custom import *
from COIM.constrain_constant_sum import *
from COIM.constrain_add_scalar import *
from COIM.constrain_mul_scalar import *

class ConstrainOperator:
	"""
	Class to orchestrate many rules sequencially
	"""
	def __init__(self, name="COIM", print_width=30):
		"""
		(str, int)->None
		Initiallize class parameters
		"""
		self.name=name
		self.operations=[]
		self.print_width=print_width
		self._encoded=False
		self._decoded=False

	def add_rule(self, rule, index=None):
		"""
		(Constrain, int)->None
		Insert a rule in the series in the specified position.
		"""
		if index:
			assert isinstance(index, int) and index>=0 and index<len(self.operations), "Index is not valid"
			self.operations=self.operations[:index]+[rule]+self.operations[index:]
		else:
			self.operations.append(rule)

	def show_rules(self, table=None):
		"""
		(PrettyTable)->PrettyTable
		Create table showing the rules in the sequence
		"""
		if not table: table=PrettyTable()
		table.title=f"{self.name} rules"
		table.field_names=["Position", "Constrain"]
		table.min_width=self.print_width
		rules_list=[[i, op.format_rule()] for i, op in zip(range(1, len(self.operations)+1), self.operations)]
		table.add_rows(rules_list)
		return table

	def show_encode(self, table=None):
		"""
		(PrettyTable)->PrettyTable
		Create table showing the gains on the encoding phase
		"""
		if not self._encoded: return
		if not table: table=PrettyTable()
		table.title=f"{self.name} encode results"
		table.field_names=["Variable", "Value"]
		table.min_width=self.print_width
		table.add_row(["Variation reduction", f"{round(100*(self._variance_gain), 3)} %"])
		table.add_row(["Columns reduction", f"{round(100*(self._col_gain), 3)} %"])
		return table

	def show_decode(self, table=None):
		"""
		(PrettyTable)->PrettyTable
		Create table showing the gains on the decoding phase
		"""
		if not self._decoded: return
		if not table: table=PrettyTable()
		table.title=f"{self.name} decode results"
		table.field_names=["Variable", "Value"]
		table.min_width=self.print_width
		table.add_row(["Error/mean value reduction", f"{round(100*(self._error_value_gain), 3)} %"])
		return table

	def summary(self):
		"""
		(None)->None
		Print the summary of the model
		"""
		t_rules=str(self.show_rules())
		t_encode=str(self.show_encode())
		t_decode=str(self.show_decode())
		result=t_rules
		if self._encoded: result+=t_encode[t_encode.index("\n"):]
		if self._decoded: result+=t_decode[t_decode.index("\n"):]
		print(result)

	def encode_dataframe(self, df):
		"""
		(DataFrame)->DataFrame
		Apply all the rules in order
		"""
		#sdf=self.validate_dataframe(df)
		self._encoded=True
		previous_variance=df.var().sum()
		previous_cols=len(df.columns)
		cont=1
		for rule in self.operations:
			df=rule.validate_dataframe(df, cont)
			df=rule.encode_dataframe(df)
			cont+=1
		later_variance=df.var().sum()
		later_cols=len(df.columns)
		self._variance_gain=1-later_variance/previous_variance
		self._col_gain=1-later_cols/previous_cols
		return df

	def decode_dataframe(self, df, errors):
		"""
		(DataFrame, DataFrame)->DataFrame, DataFrame
		Deapply all the rules in reverse order and calculate the propagated errors
		"""
		self._decoded=True
		previous_error=(errors/df.mean()).mean().mean()
		for rule in self.operations[::-1]:
			df, errors=rule.decode_dataframe(df, errors)
		later_error=(errors/df.mean()).mean().mean()
		self._error_value_gain=1-later_error/previous_error
		return df, errors

	def dump(self, path):
		"""
		(str)->None
		Saves the parameters to a pickle file
		"""
		descriptor_dict={
			"name":self.name,
			"print_width":self.print_width,
			"operations":self.operations
		}
		file=open(path, "wb")
		pickle.dump(descriptor_dict, file)
		file.close()

	def load(self, path, mode="replace"):
		"""
		(str, str)->None
		Retrieves the parameters from a pickle file
		mode can be 'replace' or 'append'
		"""
		assert mode in ["replace", "append"], "mode must be 'replace' or 'append'"
		file=open(path, "rb")
		descriptor_dict=pickle.load(file)
		file.close()
		self._encoded=False
		self._decoded=False
		if mode=="replace":
			self.name=descriptor_dict["name"]
			self.print_width=descriptor_dict["print_width"]
			self.operations=descriptor_dict["operations"]
		elif mode=="append":
			self.name-=descriptor_dict["name"]+"_"
			self.print_width=max(self.print_width, descriptor_dict["print_width"])
			self.operations.append(descriptor_dict["operations"])
