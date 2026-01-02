"""Definition of add scalar constraint."""


from COIM.constraints.constrain import Constrain


class AddScalar(Constrain):
    """General class to store the constraint rule."""

    def __init__(self, base_variable, target_variable, constant, labels=None, precision=1e-10):
        """
        Save general parameters of the rule.

        Args:
            base_variable (str): name for the base value in DataFrame
            target_variable (str): name for the target value in DataFrame
            constant (float): the difference between target_variable and base_variable
            labels (list): names for the new columns created
            precision (list): precision to be used in DataFrame validation
        """
        # Garantee parameters are consistent
        assert not labels, "Labels not needed for add_scalar"

        # Initialize the supper class
        variables = [base_variable, target_variable]
        params = [constant]
        super().__init__(variables, params, labels, precision)

        # Save appropriate parameters
        self.const_K = constant
        self.column_a = base_variable
        self.column_b = target_variable

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

        # Check if rule conforms
        df["calculated_rule"] = df[self.column_b] - (df[self.column_a] + self.const_K)
        df = df[abs(df["calculated_rule"]) > self.precision]
        if len(df) != 0:
            message = f"The following lines does not conform to rule {position}\n{df}"
            raise ValueError(message)

    def format_rule(self):
        """
        Return a string describing the rule.

        Returns:
            rule (str): The string with the mathematical expression for the contraint
        """
        return f"{self.column_a}+{self.const_K}={self.column_b}"

    def encode_dataframe(self, df):
        """
        Apply the developed formulas to reduce the dataframe columns.

        Args:
            df (pd.DataFrame): The input DataFrame to be encoded

        Returns:
            df (pd.DataFrame): The encoded DataFrame
        """
        df.drop(columns=self.column_b, inplace=True)
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
        df[self.column_b] = df[self.column_a] + self.const_K
        errors[self.column_b] = errors[self.column_a]
        return df, errors
