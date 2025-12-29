"""Base class for definition of a constraint."""


class Constrain:
    """General class to store the rules."""

    def __init__(self, variables, params, labels=None, precision=1e-10):
        """
        Save general parameters of the rule.

        Args:
            variables (list): variables used in the contraint
            params (list): parameters which define the contraint
            labels (list): names for the new columns created
            precision (list): precision to be used in DataFrame validation
        """
        self.variables = variables
        self.params = params
        self.labels = labels
        self.precision = precision

    def validate_dataframe(self, df):
        """
        Check if the rule is attended by the dataframe.

        Must return the complete dataframe.
        If there are any inconsistencies, must raise an error.

        Args:
            df (pd.DataFrame): The input DataFrame to be validated

        Returns:
            df (pd.DataFrame): The input DataFrame unmodified
        """
        return df

    def format_rule(self):
        """
        Return a string describing the rule.

        Returns:
            rule (str): The string with the mathematical expression for the contraint
        """
        rule = "Description"
        return rule

    def encode_dataframe(self, df):
        """
        Apply the developed formulas to reduce the dataframe columns.

        Args:
            df (pd.DataFrame): The input DataFrame to be encoded

        Returns:
            df (pd.DataFrame): The encoded DataFrame
        """
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
        return df, errors
