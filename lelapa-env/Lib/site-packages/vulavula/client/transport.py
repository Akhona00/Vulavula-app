import base64
import os
import uuid
import requests

from vulavula.common.response_handler import APIResponseHandler
from vulavula.config import settings


class Transport:
    """
        Manages file transportation functionalities for the Vulavula API. This class provides methods
        for uploading files to the server.

        The Transport class is essential for operations that involve file handling, such as uploading
        documents, images, or other media types that may be required for processing by other components
        of the API, such as the Transcribe service.

        Parameters:
            client_token (str): The API token required for authenticating all requests.
            base_url (str): The base URL for the API endpoints.
            session (requests.Session): The session used for HTTP requests to optimize connection reuse.

        Example:
            transport_client = Transport("your_api_token", "https://beta-vulavula-services.lelapa.ai/api/v1/")
            upload_result = transport_client.upload_file("path/to/file.mp3")
            print(upload_result)
    """
    def __init__(self, client_token,  base_url=None, session=None):
        self.base_url = base_url if base_url else settings.BASE_URL
        self.headers = {
            "X-CLIENT-TOKEN": client_token,
            "Content-Type": "application/json"
        }
        self._handle_response = APIResponseHandler.handle_response
        self.session = session if session else requests.Session()
        self.session.headers.update(self.headers)

    def upload_file(self, file_path: str):
        """
        Uploads a file to the server and Returns the upload ID received from the server which can be used for further processing or retrieval actions.

        Parameters:
            file_path (str): The full path to the file that needs to be uploaded.

        Returns:
            dict: The response from the server typically containing an 'upload_id' which is used to identify the file in subsequent operations.

        Raises:
            FileNotFoundError: If the file at the specified `file_path` does not exist.
            requests.exceptions.RequestException: For network-related errors during the file upload.

        Example:
            try:
                file_path = '/path/to/your/file.wav'
                upload_response = self.upload_file(file_path)
                print("Upload successful, ID:", upload_response['upload_id'])
            except FileNotFoundError:
                print("The file was not found at the specified path.")
            except requests.exceptions.RequestException as e:
                print("An error occurred during file upload:", str(e))
        """
        url = f"{self.base_url}/transport/file-upload"

        # Get file size
        file_size = os.path.getsize(file_path)

        # Generate file name
        _, file_extension = os.path.splitext(file_path)

        random_filename = str(uuid.uuid4())

        file_name = f"{random_filename}{file_extension}"

        with open(file_path, 'rb') as file:
            file_content = file.read()

            # Encode file content
            encoded_content = base64.b64encode(file_content)

            # Decode bytes to string
            encoded_string = encoded_content.decode()

            transport_request_body = {
                "file_name": file_name,
                "audio_blob": encoded_string,
                "file_size": file_size,
            }
            response = self.session.post(url, headers=self.headers, json=transport_request_body, )
            return self._handle_response(response)
