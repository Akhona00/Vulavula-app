from dataclasses import dataclass
from typing import Dict, List, Optional
@dataclass
class CreateKnowledgeBaseRequest:
    collection: str
@dataclass
class CreateDocumentsRequest:
    documents: List[str]
    collection: Optional[str]
    language: str
@dataclass
class SearchQueryRequest:
    query: str
    language: Optional[str]
    collection: str

@dataclass
class QueryKnowledgeBase:
    query: str

@dataclass
class UploadPDFRequest:
    file: bytes
    filename: str