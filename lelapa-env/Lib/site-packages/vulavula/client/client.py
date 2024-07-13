
from typing import Optional

import requests
from uuid import UUID

from vulavula.client.nlu import NLU
from vulavula.client.sentiment import Sentiment
from vulavula.client.transcribe import Transcribe
from vulavula.client.transport import Transport
from vulavula.client.vulavula_search import VulavulaSearch
from vulavula.client.translation import Translation
from vulavula.config import settings
from vulavula.models.types import (EntityRecognitionRequestData, SentimentAnalysisRequestData, \
    IntentClassificationRequestData , CreateKnowledgeBaseRequest,TranslationRequest)


class VulavulaClient:
    """
    A client for interacting with the Vulavula API.

    This client provides access to a variety of services such as natural language processing,
    sentiment analysis, transcription, and file transport. It simplifies the interaction with different
    components of the Vulavula API by encapsulating them into easy-to-use sub-client classes.

    Parameters:
        client_token (str): The API token used for authenticating with the API.
        base_url (Optional[str]): The base URL for the API endpoints. If not provided,
                                  defaults to the URL specified in the project's settings (add in .env).

    Attributes:
        base_url (str): The API base URL used for all requests.
        session (requests.Session): The session used for HTTP requests to optimize connection reuse.
        headers (dict): Default headers to include in every API request, including the authentication token.
        nlu (NLU): Sub-client for Natural Language Understanding features.
        sentiments (Sentiment): Sub-client for sentiment analysis features.
        transcribe_client (Transcribe): Sub-client for audio transcription services.
        transport (Transport): Sub-client for file transport services.

    Usage:
         client = VulavulaClient("<INSERT_TOKEN>")
         response = client.sentiments.get_sentiments({"encoded_text": "I hate the rain. But I love the sun."})
         print(response)
    """
    def __init__(self, client_token, base_url=None):
        """
        Initializes a new instance of the VulavulaClient.

        The client can optionally accept a custom base URL.

        Args:
            client_token (str): The token required to authenticate requests to the API.
            base_url (str, optional): A custom URL to use instead of the default API URL.
        """
        self.base_url = base_url if base_url else settings.BASE_URL
        self.session = requests.Session()
        self.headers = {
            "X-CLIENT-TOKEN": client_token,
            "Content-Type": "application/json"
        }
        self.session.headers.update(self.headers)
        self.nlu = NLU(client_token, self.base_url, session=self.session)
        self.sentiments = Sentiment(client_token, self.base_url, session=self.session)
        self.transcribe_client = Transcribe(client_token, self.base_url, session=self.session)
        self.transport = Transport(client_token, self.base_url, session=self.session)
        self.search = VulavulaSearch(client_token, self.base_url, session=self.session)
        self.translation = Translation(client_token, self.base_url, session=self.session)

    def upload_file(self, file_path: str):
        return self.transport.upload_file(file_path)

    def transcribe_process(self, upload_id: UUID, webhook: Optional[str] = None, language_code: Optional[str] = None):
        return self.transcribe_client.transcribe_process(upload_id, webhook=webhook, language_code=language_code)

    def transcribe(self, file_path: str, *, webhook: Optional[str] = None, language_code: Optional[str] = None):
        return self.transcribe_client.transcribe(file_path, webhook=webhook, language_code=language_code)

    def get_transcribed_text(
            self,
            upload_id: UUID
    ):
        return self.transcribe_client.get_transcribed_text(upload_id)

    def get_sentiments(self, data: SentimentAnalysisRequestData):
        return self.sentiments.get_sentiments(data)

    def get_entities(self, data: EntityRecognitionRequestData):
        return self.nlu.get_entities(data)

    def classify(self, data: IntentClassificationRequestData):
        return self.nlu.classify(data)

    def get_intents(self, data: IntentClassificationRequestData):
        return self.nlu.get_intents(data)

    def create_knowledgebase(self, data: CreateKnowledgeBaseRequest):
        return self.search.create_collection(data)

    def create_documents(self,file_path: str, language: str=None):
        return self.search.upload_and_extract_text(file_path, language)

    def query(self,query: str, language: str=None):
        return self.search.search_query(query, language)

    def translate(self, data:TranslationRequest):
        return self.translation.translate(data)
