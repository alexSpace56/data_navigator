import chromadb
import numpy as np
import hashlib
from typing import List


class LiteEmbedder:
    def __init__(self, dimension=384):
        self.dimension = dimension

    def encode(self, texts: List[str]) -> List[List[float]]:
        return [
            np.random.normal(0, 0.1, self.dimension).tolist()
            for text in texts
        ]


embedder = LiteEmbedder()
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="database_schema")


def index_database():
    from database import get_database_schema
    schema = get_database_schema()

    documents, metadatas, ids = [], [], []

    for table in schema:
        desc = f"Таблица {table['table_name']}: {', '.join(col['name'] for col in table['columns'])}"
        documents.append(desc)
        metadatas.append({"type": "table", "name": table['table_name']})
        ids.append(f"table_{table['table_name']}")

    embeddings = embedder.encode(documents)
    collection.add(documents=documents, metadatas=metadatas, ids=ids, embeddings=embeddings)
    return len(documents)


def query_database(query: str, n_results: int = 5):
    query_embedding = embedder.encode([query])
    return collection.query(query_embeddings=query_embedding, n_results=n_results)