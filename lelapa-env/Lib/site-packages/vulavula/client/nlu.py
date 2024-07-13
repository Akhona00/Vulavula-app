from typing import Dict, Union, List

import requests

from vulavula.common.response_handler import APIResponseHandler
from vulavula.config import settings
from vulavula.models.types import EntityRecognitionRequestData, IntentClassificationRequestData


class NLU:
    """
    Handles Natural Language Understanding (NLU) functionalities for the Vulavula API, including entity recognition
    and intent classification. This class is part of the VulavulaClient (but can be imported and used independently),
    using the same session, headers, and base URL configured in the main client.

    Parameters:
        client_token (str): The API token required for authenticating all requests.
        base_url (str): The base URL for the API endpoints.
        session (requests.Session): The session used for HTTP requests to optimize connection reuse.

    Example:
         nlu_client = NLU("your_api_token", "https://beta-vulavula-services.lelapa.ai/api/v1/")
         entities = nlu_client.get_entities("Check the status of my flight to New York.")
         print(entities)
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

    def get_entities(self, data: Union[Dict[str, str], EntityRecognitionRequestData]):
        """
        Sends a request to the API to perform entity recognition on the provided text.

        Parameters:
            data (EntityRecognitionRequestData): An instance of EntityRecognitionRequestData containing the text to be processed.

        Returns:
            dict: The response from the server after processing the entity recognition request.

        Example:
            data = {"encoded_text"="President Ramaphosa gaan loop by Emfuleni Municipality."}
            try:
                entities_result = client.get_entities(data)
                print("Identified Entities:", entities_result)
            except Exception as e:
                print(f"Error during entity recognition: {e}")
        """

        if isinstance(data, EntityRecognitionRequestData):
            data = data.__dict__

        url = f"{self.base_url}/entity_recognition/process"
        response = self.session.post(url, headers=self.headers, json=data)
        return self._handle_response(response)

    def classify(self,
                 data: Union[Dict[str, List[Dict[str, str]]], List[str], IntentClassificationRequestData]):
        """
        Trains on the provided examples and predicts intents for the provided inputs.

        Parameters:
            data (IntentClassificationRequestData): An instance containing training examples and input queries.

        Returns:
            List[IntentClassificationResponse]: A list of IntentClassificationResponse objects, each containing a list of IntentProbability
                                          objects with predicted intents and their scores.

        Example:
            examples = [
                IntentExample(intent="greeting", example="Hello!"),
                IntentExample(intent="greeting", example="Hi there!"),
                IntentExample(intent="goodbye", example="Goodbye!"),
                IntentExample(intent="goodbye", example="See you later!")]
            inputs = ["Hey, how are you?", "I must be going now."]
            data = IntentClassificationRequestData(examples=examples, inputs=inputs)
            classification_results = client.classify(data)
            for result in classification_results:
                print(result)
        """

        if isinstance(data, IntentClassificationRequestData):
            data = data.__dict__

        url = f"{self.base_url}/classify"
        response = self.session.post(url, headers=self.headers, json=data)
        return self._handle_response(response)

    def get_intents(self, data: IntentClassificationRequestData):
        """
        Trains on the provided examples and predicts intents for the provided inputs
        """
        url = f"{self.base_url}/classify"
        response = self.session.post(url, headers=self.headers, json=data)
        return self._handle_response(response)
