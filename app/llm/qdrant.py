# app/db/qdrant.py
from qdrant_client import QdrantClient

_client = None

def get_qdrant_client():
    global _client
    if _client is None:
        _client = QdrantClient(path="./qdrant_data")
    return _client

def close_qdrant_client():
    global _client
    if _client is not None:
        _client.close()
        _client = None
