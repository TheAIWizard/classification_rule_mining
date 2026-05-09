import os
import torch
from sentence_transformers import SentenceTransformer


class EmbeddingEngine:
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingEngine, cls).__new__(cls)

            # 1. Définir un dossier local pour ne plus jamais retélécharger
            # Sur Onyxia, utilise un chemin dans /home/onyxia/work/
            cache_dir = "/home/onyxia/work/hf_cache"
            os.makedirs(cache_dir, exist_ok=True)

            device = "cuda" if torch.cuda.is_available() else "cpu"
          
            print(f"--- Chargement du modèle Solon sur {device} ---")
          
            # 2. Le modèle est chargé une seule fois en RAM grâce au Singleton
            cls._model = SentenceTransformer(
                'OrdalieTech/Solon-embeddings-large-0.1',
                device=device,
                cache_folder=cache_dir
            )
            print("--- Modèle prêt ! ---")

        return cls._instance

    def encode(self, text: str):
        return self._model.encode(text, normalize_embeddings=True).tolist()


# Instance globale (Optionnel, mais pratique)
# Elle ne chargera le modèle que la première fois qu'on l'appelle
engine = EmbeddingEngine()


def get_embedding(text: str):
    return engine.encode(text)