
from typing import List, Dict, Any
from transformers import pipeline

class EntityRecognizer:
    def __init__(self, model: str):
        self.ner_pipeline = pipeline("ner", 
                                     aggregation_strategy="simple", 
                                     model=model)

    def recognize_entities(self, sentences: List[str]) -> List[Dict[str, Any]]:
        return self.ner_pipeline(sentences)
