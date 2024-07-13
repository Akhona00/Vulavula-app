from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class TranslationRequest:
    input_text: str
    source_lang: str
    target_lang: str