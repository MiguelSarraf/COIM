"""Definition of mul scalar constraint."""


from COIM.constraints.constrain import Constrain


class MulScalar(Constrain):
    """General class to store the constraint rule."""

    def __init__(self, base_variable, target_variable, constant, labels=None, precision=1e-10):
        """
        Save general parameters of the rule.

        Args:
            base_variable (str): name for the base value in DataFrame
            target_variable (str): name for the target value in DataFrame
            constant (float): the ratio between target_variable and base_variable
            labels (list): names for the new columns created
            precision (list): precision to be used in DataFrame validation
        """
        # Garantee parameters are consistent
        message = "Labels must correspond exactly to the second variables"
        assert not labels or len(labels) == 1, message

        # Initialize the supper class
        variables = [base_variable, target_variable]
        params = [constant]
        super().__init__(variables, params, labels, precision)

        # Save appropriate parameters
        self.const_K = constant
        self.column_a = base_variable
        self.column_b = target_variable
        self.labels = {self.column_a: "new_" + self.column_a if not labels else labels[0]}

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
        # Check if rule conforms
        df_filter = df[abs(df[self.column_b] - df[self.column_a] * self.const_K) > self.precision]
        if len(df_filter) != 0:
            message = f"The following lines does not conform to rule {position}\n{df_filter}"
            raise ValueError(message)

    def format_rule(self):
        """
        Return a string describing the rule.

        Returns:
            rule (str): The string with the mathematical expression for the contraint
        """
        return f"{self.column_a} * {self.const_K} = {self.column_b}"

    def encode_dataframe(self, df):
        """
        Apply the developed formulas to reduce the dataframe columns.

        a' = a if |const_K|>1 else b

        Args:
            df (pd.DataFrame): The input DataFrame to be encoded

        Returns:
            df (pd.DataFrame): The encoded DataFrame
        """
        df = df.copy()
        if abs(self.const_K) <= 1:
            df[self.labels[self.column_a]] = df[self.column_b]
        else:
            df[self.labels[self.column_a]] = df[self.column_a]
        df.drop(columns=[self.column_a, self.column_b], inplace=True)
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
        df = df.copy()
        errors = errors.copy()
        if abs(self.const_K) <= 1:
            df.rename(columns={self.labels[self.column_a]: self.column_b}, inplace=True)
            df[self.column_a] = df[self.column_b] / self.const_K
            errors.rename(columns={self.labels[self.column_a]: self.column_b}, inplace=True)
            errors[self.column_a] = errors[self.column_b] / self.const_K
        else:
            df.rename(columns={self.labels[self.column_a]: self.column_a}, inplace=True)
            df[self.column_b] = df[self.column_a] * self.const_K
            errors.rename(columns={self.labels[self.column_a]: self.column_a}, inplace=True)
            errors[self.column_b] = errors[self.column_a] * self.const_K
        return df, errors
