"""Vector store interface using ChromaDB."""
import chromadb
from chromadb.utils import embedding_functions

class VectorStore:
    def __init__(self, collection_name='documents', persist_dir='./chroma_db'):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.ef = embedding_functions.OpenAIEmbeddingFunction(model_name='text-embedding-3-small')
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.ef,
        )

    def add(self, texts, ids=None, metadatas=None):
        """Add text chunks to the vector store."""
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(texts))]
        self.collection.add(documents=texts, ids=ids, metadatas=metadatas)

    def search(self, query, n_results=5):
        """Search for similar documents."""
        results = self.collection.query(query_texts=[query], n_results=n_results)
        return results

    def count(self):
        return self.collection.count()
