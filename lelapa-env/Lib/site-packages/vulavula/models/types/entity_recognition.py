from dataclasses import dataclass


@dataclass
class EntityRecognitionRequestData:
    encoded_text: str
