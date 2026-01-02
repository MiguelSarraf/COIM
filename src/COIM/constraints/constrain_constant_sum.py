"""Definition of constant sum constraint."""


from COIM.constraints.constrain import Constrain


class ConstantSum(Constrain):
    """General class to store the constraint rule."""

    def __init__(
            self,
            variables,
            reference_variable,
            constant_sum,
            weights=1,
            labels=None,
            precision=1e-10,
    ):
        """
        Save general parameters of the rule.

        Args:
            variables (list[str]): names for all the values in DataFrame
            reference_variable (str): name for the reference value in DataFrame
            constant_sum (float): the value which the variables must sum
            weights (list[float]): the sum weights
            labels (list): names for the new columns created
            precision (list): precision to be used in DataFrame validation
        """
        # Garantee parameters are consistent
        message = "Labels must correspond exactly to the last n-1 variables"
        assert not labels or len(labels) == len(variables) - 1, message
        message = "Weights must be a number or a list matching all the variables"
        assert isinstance(weights, (int, float)) or len(weights) == len(variables), message

        # Initialize the supper class
        params = constant_sum
        super().__init__(variables, params, labels, precision)

        # Save appropriate parameters
        self.sum = constant_sum
        self.all_variables = variables[:]
        variables.remove(reference_variable)
        self.variables = variables
        self.column_a0 = reference_variable
        self.weights = (
            [weights for i in range(len(variables) + 1)]
            if isinstance(weights, (int, float))
            else weights
        )
        self.labels = {}
        if labels:
            for old, new in zip(self.variables, labels):
                self.labels[old] = new
        else:
            self.labels = {old: old + "'" for old in self.variables}

    def validate_dataframe(self, df, position):
        """
        Check if the rule is attended by the dataframe.

        Must return the complete dataframe.
        sum_{i=0}^N W_i * a_i = K

        Args:
            df (pd.DataFrame): The input DataFrame to be validated
            position (int): The position of the rule inside the operator

        Raises:
            ValueError: If there are any non-conformant lines
        """
        df = df.copy()
        df["sum"] = 0
        for weight, var in zip(self.weights, self.all_variables):
            assert var in df, f"Variable {var} not in dataframe"
            df["sum"] += df[var] * weight  # sum_{i=0}^N W_i * a_i
            df["diff"] = abs(df["sum"] - self.sum)  # sum_{i=0}^N W_i * a_i - K

        # Check if rule conforms
        df_filter = df[df["diff"] > self.precision]
        if len(df_filter) != 0:
            print(self.sum)
            message = f"The following lines does not conform to rule {position}\n{df_filter}"
            raise ValueError(message)

    def format_rule(self):
        """
        Return a string describing the rule.

        Returns:
            rule (str): The string with the mathematical expression for the contraint
        """
        rule = ""
        for weight, var in zip(self.weights, self.all_variables):
            if weight == 1:
                rule += f"{var}+"
            else:
                rule += f"{weight}*{var}+"
        return rule[:-1] + f"={self.sum}"

    def encode_dataframe(self, df):
        """
        Apply the developed formulas to reduce the dataframe columns.

        a_i'=\frac{a_i}{a_0 K}

        Args:
            df (pd.DataFrame): The input DataFrame to be encoded

        Returns:
            df (pd.DataFrame): The encoded DataFrame
        """
        for var in self.variables:
            df[self.labels[var]] = df[var] / (self.sum * df[self.column_a0])
        df.drop(columns=self.variables + [self.column_a0], inplace=True)
        return df

    def decode_dataframe(self, df, errors):
        """
        Apply the reverse formulas to restore the original columns and propagate the errors.

        Args:
            df (pd.DataFrame): Encoded values outputed from the inferential model
            errors (pd.DataFrame): Errors for each encoded field

        Returns:
            df (pd.DataFrame): Decoded values, true outputs from the inferential model
            errors (pd.DataFrame): Errors for each decoded true field
        """
        # Calculate sums
        df["sum"] = 0
        errors["sum"] = 0
        for weight, var in zip(self.weights[1:], self.variables):
            # sum_{i=1}^N W_i * a_i
            df["sum"] += df[self.labels[var]] * weight
            # sum_{j=1}^NW_j^2*Delta a_j'^2
            errors["sum"] += errors[self.labels[var]] ** 2 * weight ** 2

        # Retrieve variables
        # a_0={K}/{W_0+K*sum_{i=1}^N W_i * a_i'}
        df[self.column_a0] = self.sum / (self.weights[0] + self.sum * df["sum"])
        # a_i=a_i'a_0K
        for var in self.variables:
            df[var] = df[self.labels[var]] * df[self.column_a0] * self.sum

        # Propagate errors
        means = df.aggregate("mean")
        # Delta a_0=a_0^2*sqrt{sum_{j=1}^NW_j^2*Delta a_j'^2}
        errors[self.column_a0] = (means[self.column_a0] ** 2) * (errors["sum"] ** .5)
        # Delta a_i=|(K-W_i*a_i)/(a_0W_i)|*sqrt{a_0^4W_i^2*Delta a_i'^2+Delta a_0^2}
        for weight, var in zip(self.weights[1:], self.variables):
            factor = (self.sum - weight * means[var]) / (means[self.column_a0] * weight)
            error_sum = (
                means[self.column_a0] ** 4 * weight ** 2 * errors[self.labels[var]] ** 2 +
                errors[self.column_a0] ** 2
            )
            errors[var] = abs(factor) * error_sum ** .5

        # Remove unnecessary columns
        df.drop(columns=[self.labels[var] for var in self.variables] + ["sum"], inplace=True)
        errors.drop(columns=[self.labels[var] for var in self.variables] + ["sum"], inplace=True)
        return df, errors
