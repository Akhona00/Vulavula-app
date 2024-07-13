from dataclasses import dataclass


@dataclass
class SentimentAnalysisRequestData:
    encoded_text: str
