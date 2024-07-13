from typing import Union, Dict
from vulavula.common.response_handler import APIResponseHandler
from vulavula.config import settings
from vulavula.models.types import CreateKnowledgeBaseRequest
import requests
import os
import logging
class VulavulaSearch:

    def __init__(self, client_token,  base_url=None, session=None):
        self.base_url = base_url if base_url else settings.BASE_URL
        self.headers = {
            "X-CLIENT-TOKEN": client_token,
            "accept": "application/json"
        }
        self.client_token= client_token
        self._handle_response = APIResponseHandler.handle_response
        self.session = session if session else requests.Session()
        self.session.headers.update(self.headers)
        self.collection = None
        self.logger = logging.getLogger("vulavulaSearch")

    def create_collection(self, data: Union[str, CreateKnowledgeBaseRequest]):
        """
        Sends a request to the API to create a knowledge base with the provided data.

        Parameters:
            data (Union[str, CreateKnowledgeBaseRequest]): An instance of CreateKnowledgeBaseRequest containing the data to create a knowledge base.
                                             This ensures that the 'collection' keys exist.

        Returns:
            dict: The response from the server after processing the knowledge base creation request.

        Example:
            data = CreateKnowledgeBaseRequest(collection="myCollection")
            try:
                kb_result = client.create_knowledge_base(data)
                print("Knowledge Base Creation Result:", kb_result)
            except Exception as e:
                print(f"Error during knowledge base creation: {e}")
        """
        if isinstance(data, CreateKnowledgeBaseRequest):
            data = data.__dict__
        url = f"{self.base_url}/search/create-knowledgebase"
        response = self.session.post(url, headers=self.headers, json=data)
        self.collection = data['collection']
        return self._handle_response(response)

    def upload_and_extract_text(self, file_path: str, language: str = None) -> dict:
        # Upload the file
        upload_url = f"{self.base_url}/search/upload-file"

        if not os.path.isfile(file_path):
            self.logger.info(f"File does not exist: {file_path}")
            return {"error": "File not found"}

        try:
            with open(file_path, "rb") as file:
                files = {"file": (file_path, file, "application/pdf")}
                upload_response = requests.post(upload_url, headers=self.headers, files=files)

            if upload_response.status_code != 200:
                self.logger.info(f"Failed to upload file. Status code: {upload_response.status_code}")
                return self._handle_response(upload_response)

            # Assuming the response contains the extracted documents
            documents = upload_response.json().get("documents", [])

            # Create documents with the extracted text
            create_documents_url = f"{self.base_url}/search/create-documents"
            data = {
                "webhook": "string",
                "documents": documents,
                "language": language,
                "collection": self.collection
            }

            create_response = requests.post(create_documents_url, headers=self.headers, json=data)

            if create_response.status_code == 200:
                self.logger.info("Documents created successfully.")
            else:
                self.logger.info(f"Failed to create documents. Status code: {create_response.status_code}")

            return self._handle_response(create_response)

        except Exception as e:
            self.logger.info(f"An error occurred: {e}")
            return {"error": str(e)}

    def search_query(self, query: str, language: str = None) -> dict:
        url = f"{self.base_url}/search/search"
        data = {
            "query": query,
            "webhook": "string_url",
            "language": language,
            "collection": self.collection
        }
        headers = {
            "accept": "application/json",
            "X-CLIENT-TOKEN": self.client_token
        }
        response = requests.post(url, headers=headers, json=data)
        return self._handle_response(response)