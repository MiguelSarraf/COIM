"""Definition of custom constraint."""


from COIM.constraints.constrain import Constrain


class Custom(Constrain):
    """General class to store the constraint rule."""

    def __init__(
            self,
            variables,
            validate_function,
            format_function,
            encode_function,
            decode_function,
            labels=None,
            precision=1e-10,
    ):
        """
        Save general parameters of the rule.

        Args:
            variables (list[str]): names for all the values in DataFrame
            validate_function (iterable): a function that implements custom rule validation
            format_function (iterable): a function that implements rule string formatting
            encode_function (iterable): a function that implements custom rule encoding
            decode_function (iterable): a function that implements custom rule decoding
            labels (list): names for the new columns created
            precision (list): precision to be used in DataFrame validation
        """
        # Initialize the supper class
        params = validate_function, format_function, encode_function, decode_function
        super().__init__(variables, params, labels, precision)

        # Save appropriate parameters
        self.validate_function = validate_function
        self.format_function = format_function
        self.encode_function = encode_function
        self.decode_function = decode_function
        self.labels = labels

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
        self.validate_function(df, self.variables, self.labels, self.precision, position)

    def format_rule(self):
        """
        Return a string describing the rule.

        Returns:
            rule (str): The string with the mathematical expression for the contraint
        """
        return self.format_function(self.variables, self.labels)

    def encode_dataframe(self, df):
        """
        Apply the developed formulas to reduce the dataframe columns.

        Args:
            df (pd.DataFrame): The input DataFrame to be encoded

        Returns:
            df (pd.DataFrame): The encoded DataFrame
        """
        df = df.copy()
        return self.encode_function(df, self.variables, self.labels)

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
        return self.decode_function(df, self.variables, self.labels, errors)
