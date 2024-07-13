from typing import Optional
from uuid import UUID
import requests

from vulavula.client.transport import Transport
from vulavula.common.error_handler import VulavulaError
from vulavula.common.response_handler import APIResponseHandler
from vulavula.config import settings


class Transcribe:
    """
    Manages transcription services provided by the Vulavula API. This class is designed to handle
    the conversion of speech to text, enabling users to transcribe audio files efficiently.

    The Transcribe class supports operations like uploading audio files for transcription and retrieving
    transcribed text.

    Parameters:
        client_token (str): The API token required for authenticating all requests.
        base_url (str): The base URL for the API endpoints.
        session (requests.Session): The session used for HTTP requests to optimize connection reuse.

    Example:
         transcribe_client = Transcribe("your_api_token", "https://beta-vulavula-services.lelapa.ai/api/v1/")
         transcription_result = transcribe_client.transcribe("path/to/audio/file.mp3")
         print(transcription_result)
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
        self.transport = Transport(client_token, self.base_url, self.session)

    def transcribe_process(self, upload_id: UUID, *, webhook: Optional[str] = None, language_code: Optional[str] = None):
        """
        Sends a request to transcribe an already uploaded file, identified by the upload ID.
        An optional webhook URL can be specified to receive notifications upon transcription completion.

        Parameters:
            upload_id (UUID): The unique identifier for the uploaded file that needs to be transcribed.
            language_code (Optional[str]): The language code for the uploaded file
            webhook (Optional[str]): The URL to which transcription completion notifications will be sent if provided.
                                     The server will POST the transcription results to this URL.

        Returns:
            dict: The response from the server after processing the transcription request.
                  This typically includes status information and details of the transcription.

        Example:
            upload_id = UUID('123e4567-e89b-12d3-a456-426614174000')
            try:
                # Example without using a webhook
                result = client.transcribe_process(upload_id)
                print("Transcription submitted, no webhook used:", result)

                # Example with a webhook
                webhook_url = "http://example.com/webhook/"
                result_with_webhook = client.transcribe_process(upload_id, webhook_url)
                print("Transcription submitted, webhook will receive the output:", result_with_webhook)
            except Exception as e:
                print(f"Error during transcription process: {e}")
        """
        url = f"{self.base_url}/transcribe/process/{upload_id}"
        json_data = {}
        if language_code:
            json_data["language_code"] = language_code
        if webhook:
            json_data["webhook"] = webhook
        response = self.session.post(
            url,
            headers=self.headers,
            json=json_data
        )
        return self._handle_response(response)

    def transcribe(self, file_path: str, *, webhook: Optional[str] = None, language_code: Optional[str] = None):
        """
        Uploads a file to the server and automatically initiates the transcription process using the resulting upload
        ID. Optionally, a webhook URL can be specified to receive notifications when the transcription is complete.

        Parameters:
            file_path (str): The path to the file that needs to be transcribed.
            language_code (Optional[str]): The language code for the uploaded file.
            webhook (Optional[str]): The URL to which transcription  completion notifications should be sent.
                                    If provided, the server will send a POST request to this URL upon completion of the
                                    transcription.

        Returns:
            dict: The response from the transcription process, typically containing details about the transcription request.

        Raises:
            VulavulaError: If the file fails to upload or if the upload ID cannot be retrieved from the response.

        Example:
            try:
                result = client.transcribe("path/to/audio.wav", "http://example.com/webhook/")
                print(result)
            except VulavulaError as e:
                print(f"An error occurred: {e}")
        """
        upload_response = self.transport.upload_file(file_path)
        upload_id = upload_response.get('upload_id')
        if upload_id:
            return upload_id, self.transcribe_process(upload_id, webhook=webhook, language_code=language_code)
        else:
            raise VulavulaError("Failed to upload file and retrieve upload ID.")

    def get_transcribed_text(
            self,
            upload_id: UUID
    ):
        """
        Fetches the transcribed text for a given upload.

        Parameters:
            upload_id (UUID): The UUID of the uploaded file.

        Returns:
            dict: The response from the server after processing the transcription request.
        """
        url = f"{self.base_url}/transcribe/{upload_id}/get"
        response = self.session.post(url, headers=self.headers)
        return self._handle_response(response)
