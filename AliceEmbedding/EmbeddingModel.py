# give me a sentencetransformer template with class
from typing import Optional
from sentence_transformers import SentenceTransformer

class AliceEmbedding:
    def __init__(self, embedding_model: Optional[str] = "all-MiniLM-L6-v2"):
        self.embedding_model = SentenceTransformer(embedding_model)
        
    def embed(self, sentence: str):
        return self.embedding_model.encode(sentence)