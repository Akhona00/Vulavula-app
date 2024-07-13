import json


class VulavulaError(Exception):
    """Custom exception class for Vulavula API errors."""

    def __init__(self, message=None, error_data=None):
        """
        Initialize with an optional error message and a list of errors.

        :param message: Optional error message to describe the error.
        :param errors: Optional list of errors or additional details.
        """
        super().__init__(message)
        self.message = message
        self.error_data = error_data if error_data is not None else {"message": message}

    def __str__(self):
        """
        String representation of the error, returns the error message and optionally the JSON string of the error data.

        :return: A string describing the exception, with optional JSON structured data.
        """
        if self.error_data:
            return f"{self.message} - Details: {json.dumps(self.error_data)}"
        return self.message
