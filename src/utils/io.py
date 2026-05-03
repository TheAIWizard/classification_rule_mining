import os
from qdrant_client import QdrantClient


def get_qdrant_client() -> QdrantClient:
    """
    Initializes and returns the Qdrant client.
    """
    return QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        port=443,
        https=True,
    )
