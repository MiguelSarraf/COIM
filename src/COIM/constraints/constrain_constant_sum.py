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

        Args:
            df (pd.DataFrame): The input DataFrame to be validated
            position (int): The position of the rule inside the operator

        Raises:
            ValueError: If there are any non-conformant lines
        """
        df = df.copy()

        # Check if rule conforms: Σ(W_i * a_i) = K

        # Iterate all variables adding their values
        df["sum"] = 0
        for weight, var in zip(self.weights, self.all_variables):
            assert var in df, f"Variable {var} not in dataframe"
            df["sum"] += df[var] * weight  # Σ(W_i * a_i)

        df["diff"] = abs(df["sum"] - self.sum)  # Σ(W_i * a_i) - K
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
        rule = "+".join(
            [
                var
                if weight == 1
                else f"{weight}*{var}"
                for weight, var in zip(
                    self.weights,
                    self.all_variables,
                )
            ],
        )
        return rule + f"={self.sum}"

    def encode_dataframe(self, df):
        """
        Apply the developed formulas to reduce the dataframe columns.

        Args:
            df (pd.DataFrame): The input DataFrame to be encoded

        Returns:
            df (pd.DataFrame): The encoded DataFrame
        """
        # a_i' = a_i/(a_0 * K)
        for var in self.variables:
            df[self.labels[var]] = df[var] / (self.sum * df[self.column_a0])
        df.drop(columns=self.all_variables, inplace=True)
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
            # Σ(W_i * a_i')
            df["sum"] += df[self.labels[var]] * weight
            # Σ(W_j^2 * Δa_j'^2)
            errors["sum"] += errors[self.labels[var]] ** 2 * weight ** 2

        # Retrieve variables

        # a_0 = K/(W_0 + K * Σ(W_i * a_i'))
        df[self.column_a0] = self.sum / (self.weights[0] + self.sum * df["sum"])

        # a_i = a_i' * a_0 * K
        for var in self.variables:
            df[var] = df[self.labels[var]] * df[self.column_a0] * self.sum

        # Propagate errors

        # As the errors formulas uses the values for the variables themselves, each line in the
        # output would have a individual error. To avoid this boredom, I chose to calculate a
        # single error with the mean of the variable values. This was, obviously, a questionable
        # choice and I did not study the impact of this strategy at the time of implementation.
        # TODO: Study the difference between the error calculation methods and make it a parameter.
        means = df.aggregate("mean")

        # Δa_0 = a_0^2 * √(Σ(W_j^2 * Δa_j'^2))
        errors[self.column_a0] = (means[self.column_a0] ** 2) * (errors["sum"] ** .5)

        # Δa_i = |(K - W_i * a_i) / (a_0 * W_i)| * √(a_0^4 * W_i^2 * Δa_i'^2 + Δa_0^2)
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
