from dataclasses import dataclass
from typing import List


@dataclass
class IntentExample:
    """
    Represents a training example for the classification model.

    Attributes:
        intent (str): The intent label associated with the example.
        example (str): The text example that illustrates the intent.
    """
    intent: str
    example: str


@dataclass
class IntentClassificationRequestData:
    """
    Encapsulates the data needed to train and predict intents using the classification model.

    Attributes:
        examples (List[Example]): A list of Example instances for training the model.
        inputs (List[str]): A list of input sentences for which the model should predict intents.
    """
    examples: List[IntentExample]
    inputs: List[str]


@dataclass
class IntentProbability:
    """
    Represents the probability score associated with a specific intent for a given input.

    Attributes:
        intent (str): The intent label.
        score (float): The probability score (0 to 1) representing the confidence of the intent prediction.
    """
    intent: str
    score: float


@dataclass
class IntentClassificationResponse:
    """
    Represents the response structure for intent predictions, containing probabilities of different intents.

    Attributes:
        probabilities (List[IntentProbability]): A list of IntentProbability instances that detail the predicted intents
                                                 and their associated scores for a single input.
    """
