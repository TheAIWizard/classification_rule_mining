from sentence_transformers import SentenceTransformer
import torch


class EmbeddingEngine:
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingEngine, cls).__new__(cls)
            # Chargement du modèle Solon
            device = "cuda" if torch.cuda.is_available() else "cpu"
            cls._model = SentenceTransformer(
                'OrdalieTech/Solon-embeddings-large-0.1', 
                device=device
            )
        return cls._instance

    def encode(self, text: str):
        # Solon performe mieux avec la normalisation pour la similarité cosinus
        return self._model.encode(text, normalize_embeddings=True).tolist()


def get_embedding(text: str):
    return EmbeddingEngine().encode(text)