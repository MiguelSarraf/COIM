"""
This module defines the ConstrainOperator class.

This class is responsible for creating a sequence of contraints and operating them.
"""

import pickle

from prettytable import PrettyTable


class ConstrainOperator:
    """Class to orchestrate many constraints rules sequencially."""

    def __init__(self, name="COIM", print_width=30):
        """
        Initiallize class parameters.

        Args:
            name (str): Constraint operator model name
            print_width (int): Line width to be used to print statistics
        """
        self.name = name
        self.operations = []
        self.print_width = print_width
        self.execution_parameters = {
            "encoded": False,
            "decoded": False,
        }

    def add_rule(self, rule, index=None):
        """
        Insert a rule in the series in the specified position.

        Args:
            rule (Constrain): Constraint to be inserted into the operator
            index (int): Position the constraint must occupy
        """
        if index:
            assert (
                isinstance(index, int) and
                0 <= index < len(self.operations)
            ), "Index is not valid"
            self.operations = self.operations[:index] + [rule] + self.operations[index:]
        else:
            self.operations.append(rule)

    def show_rules(self, table=None):
        """
        Create table showing the rules in the sequence.

        Args:
            table (PrettyTable): PrettyTable with previous output values, if present

        Returns:
            table (PrettyTable): PrettyTable with new values appended
        """
        if not table:
            table = PrettyTable()
        table.title = f"{self.name} rules"
        table.field_names = ["Position", "Constrain"]
        table.min_width = self.print_width
        rules_list = [
            [
                i,
                op.format_rule(),
            ]
            for i, op in
            zip(
                range(
                    1,
                    len(self.operations) + 1,
                ),
                self.operations,
            )
        ]
        table.add_rows(rules_list)
        return table

    def show_encode(self, table=None):
        """
        Create table showing the gains on the encoding phase.

        Args:
            table (PrettyTable): PrettyTable with previous output values, if present

        Returns:
            table (PrettyTable): PrettyTable with new values appended
        """
        if not self.execution_parameters["encoded"]:
            return table
        if not table:
            table = PrettyTable()
        table.title = f"{self.name} encode results"
        table.field_names = ["Variable", "Value"]
        table.min_width = self.print_width
        table.add_row(
            [
                "Variation reduction",
                f"{round(100*(self.execution_parameters['variance_gain']), 3)} %",
            ],
        )
        table.add_row(
            [
                "Columns reduction",
                f"{round(100*(self.execution_parameters['col_gain']), 3)} %",
            ],
        )
        return table

    def show_decode(self, table=None):
        """
        Create table showing the gains on the decoding phase.

        Args:
            table (PrettyTable): PrettyTable with previous output values, if present

        Returns:
            table (PrettyTable): PrettyTable with new values appended
        """
        if not self.execution_parameters["decoded"]:
            return table
        if not table:
            table = PrettyTable()
        table.title = f"{self.name} decode results"
        table.field_names = ["Variable", "Value"]
        table.min_width = self.print_width
        table.add_row(
            [
                "Error/mean value reduction",
                f"{round(100*(self.execution_parameters['error_value_gain']), 3)} %",
            ],
        )
        return table

    def summary(self):
        """Print the summary of the model."""
        t_rules = str(self.show_rules())
        t_encode = str(self.show_encode())
        t_decode = str(self.show_decode())
        result = t_rules
        if self.execution_parameters["encoded"]:
            result += t_encode[t_encode.index("\n"):]
        if self.execution_parameters["decoded"]:
            result += t_decode[t_decode.index("\n"):]
        print(result)

    def encode_dataframe(self, df):
        """
        Apply all the rules in order.

        Args:
            df (pd.DataFrame): DataFrame with true values

        Returns:
            df (pd.DataFrame): DataFrame with encoded values
        """
        self.execution_parameters["encoded"] = True
        previous_variance = df.var().sum()
        previous_cols = len(df.columns)
        cont = 1
        for rule in self.operations:
            df = rule.validate_dataframe(df, cont)
            df = rule.encode_dataframe(df)
            cont += 1
        later_variance = df.var().sum()
        later_cols = len(df.columns)
        self.execution_parameters["variance_gain"] = 1 - later_variance / previous_variance
        self.execution_parameters["col_gain"] = 1 - later_cols / previous_cols
        return df

    def decode_dataframe(self, df, errors):
        """
        Deapply all the rules in reverse order and calculate the propagated errors.

        Args:
            df (pd.DataFrame): Encoded values outputed from the inferential model
            errors (pd.DataFrame): Errors for each encoded field

        Returns:
            df (pd.DataFrame): Decoded values, true outputs from the inferential model
            errors (pd.DataFrame): Errors for each decoded true field
        """
        self.execution_parameters["decoded"] = True
        previous_error = (errors / df.mean()).mean().mean()
        for rule in self.operations[::-1]:
            df, errors = rule.decode_dataframe(df, errors)
        later_error = (errors / df.mean()).mean().mean()
        self.execution_parameters["error_value_gain"] = 1 - later_error / previous_error
        return df, errors

    def dump(self, path):
        """
        Save the parameters to a pickle file.

        Args:
            path (str): is the file path to be save the model into
        """
        descriptor_dict = {
            "name": self.name,
            "print_width": self.print_width,
            "operations": self.operations,
        }
        with open(path, "wb") as file:
            pickle.dump(descriptor_dict, file)

    def load(self, path, mode="replace"):
        """
        Retrieve saved operator from a pickle file into the operator.

        Args:
            path (str): is the file path to be loaded from
            mode (str): can be 'replace' or 'append'
        """
        assert mode in ["replace", "append"], "mode must be 'replace' or 'append'"
        with open(path, "rb") as file:
            descriptor_dict = pickle.load(file)
        self.execution_parameters["encoded"] = False
        self.execution_parameters["decoded"] = False
        if mode == "replace":
            self.name = descriptor_dict["name"]
            self.print_width = descriptor_dict["print_width"]
            self.operations = descriptor_dict["operations"]
        elif mode == "append":
            self.name -= descriptor_dict["name"] + "_"
            self.print_width = max(self.print_width, descriptor_dict["print_width"])
            self.operations.append(descriptor_dict["operations"])
