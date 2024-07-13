from typing import Union, Dict

import requests

from vulavula.common.response_handler import APIResponseHandler
from vulavula.config import settings
from vulavula.models.types import SentimentAnalysisRequestData


class Sentiment:
    """
    Handles sentiment analysis for the Vulavula API, providing functionalities to analyze
    the emotional tone behind texts.

    The Sentiment class allows for the detection of sentiments in given text, facilitating
    the interpretation of tone or sentiments such as positive, negative, and neutral.

    Parameters:
        client_token (str): The API token required for authenticating all requests.
        base_url (str): The base URL for the API endpoints.
        session (requests.Session): The session used for HTTP requests to optimize connection reuse.

    Example:
        sentiment_client = Sentiment("your_api_token", "https://beta-vulavula-services.lelapa.ai/api/v1/")
        sentiment_results = sentiment_client.get_sentiments("I love using Vulavula services!")
        print(sentiment_results)
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

    def get_sentiments(self, data: Union[Dict[str, str], SentimentAnalysisRequestData]):
        """
        Sends a request to the API to perform sentiment analysis on the provided text.

        Parameters:
            data (SentimentAnalysisRequestData): An instance of SentimentAnalysisRequestData containing the text to be analyzed.
                                         This ensures that the 'encoded_text' key exists and holds a string value.

        Returns:
            dict: The response from the server after processing the sentiment analysis request.

        Example:
            data = {"encoded_text": "I love sunny days, but I hate rain."}
            try:
                sentiment_result = client.get_sentiments(data)
                print("Sentiment Analysis Result:", sentiment_result)
            except Exception as e:
                print(f"Error during sentiment analysis: {e}")
        """
        if isinstance(data, SentimentAnalysisRequestData):
            data = data.__dict__
        url = f"{self.base_url}/sentiment_analysis/process"
        response = self.session.post(url, headers=self.headers, json=data)
        return self._handle_response(response)
