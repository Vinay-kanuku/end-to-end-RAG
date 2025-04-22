from src.constants import EMBEDDING_MODEL
from langchain_huggingface import HuggingFaceEmbeddings
class Embedder:
    def __init__(self, model_name=EMBEDDING_MODEL):
        self.model = HuggingFaceEmbeddings(model_name=model_name)