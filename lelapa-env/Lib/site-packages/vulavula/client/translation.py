from typing import Union, Dict

import requests

from vulavula.common.response_handler import APIResponseHandler
from vulavula.config import settings
from vulavula.models.types import TranslationRequest


class Translation:
    """
    Handles translation for the Vulavula API, providing functionalities to translate
    text from one language to another.

    The Translation class allows for the translation of given text, facilitating
    the interpretation of text in different languages.

    Parameters:
        client_token (str): The API token required for authenticating all requests.
        base_url (str): The base URL for the API endpoints.
        session (requests.Session): The session used for HTTP requests to optimize connection reuse.

    Example:
        translation_client = Translation("your_api_token", "https://beta-vulavula-services.lelapa.ai/api/v1/")
        translation_results = translation_client.translate({
            "input_text": "this is a test",
            "source_lang": "en",
            "target_lang": "sw"
        })
        print(translation_results)
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

    def translate(self, data: Union[Dict[str, str], TranslationRequest]):
        """
        Sends a request to the API to perform translation on the provided text.

        Parameters:
            data (TranslationRequest): An instance of TranslationRequest containing the text to be translated,
                                       the source language, the target language, and an optional webhook URL.

        Returns:
            dict: The response from the server after processing the translation request.

        Example:
            data = {
                "input_text": "this is a test",
                "source_lang": "en",
                "target_lang": "sw"
            }
            try:
                translation_result = client.translate(data)
                print("Translation Result:", translation_result)
            except Exception as e:
                print(f"Error during translation: {e}")
        """
        if isinstance(data, TranslationRequest):
            data = data.__dict__
        url = f"{self.base_url}/translate/process"
        response = self.session.post(url, headers=self.headers, json=data)
        return self._handle_response(response)
