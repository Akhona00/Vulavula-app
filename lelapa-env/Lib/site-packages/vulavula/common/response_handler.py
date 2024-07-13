import requests
from vulavula.common.error_handler import VulavulaError


class APIResponseHandler:
    @staticmethod
    def handle_response(response):
        """
        Handles HTTP responses by checking the status code. If the status code is 200 or 201,
        it returns the JSON content of the response. Otherwise, it returns a JSON object with
        error details.

        Parameters:
            response (requests.Response): The HTTP response object to handle.

        Returns:
            dict: The JSON content from the HTTP response if successful.

        Raises:
            VulavulaError: If the response's status code is not 200 or 201 or other errors occur.
        """
        successful_codes = {200, 201}
        try:
            if response.status_code in successful_codes:
                return response.json()
            else:
                # Raise a VulavulaError with structured error details
                raise APIResponseHandler.create_error(response)

        except requests.exceptions.JSONDecodeError as e:
            # Raise a VulavulaError with JSON error details when JSON decoding fails
            raise APIResponseHandler.create_error(response, exception=e)

        except requests.exceptions.RequestException as req_err:
            # Raise a VulavulaError with details about general request errors
            raise APIResponseHandler.create_error(response, exception=req_err)

    @staticmethod
    def create_error(response, exception=None):
        """
        Creates a VulavulaError based on the HTTP response and optionally an exception object to include more specific error information.

        Parameters:
            response (requests.Response): The HTTP response object from which to extract error details.
            exception (Exception): Optional. The exception that was raised.

        Returns:
            VulavulaError: A VulavulaError exception with a message and error details.
        """
        error_data = {
            "error": True,
            "status_code": response.status_code,
            "message": None,  # Default to None, updated below
            "details": None  # Default to None, updated below
        }

        if exception:
            error_data["message"] = f"Request failed: {str(exception)}"
            error_data["details"] = str(exception)
        else:
            error_content = response.content if response.content else b'{"message": "No detailed error message available"}'
            error_data["message"] = f"API error: {response.status_code}"
            error_data["details"] = error_content.decode() if error_content else "No detailed error message available"

        return VulavulaError("Vulavula errors", error_data=error_data)

