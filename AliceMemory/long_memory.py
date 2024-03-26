# Get AliceCore
import sys
sys.path.insert(0, '../AliceCore')

# Python packages
from typing import Optional
from uuid import uuid4

# Qdrant
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

# AliceCore
from AliceCore.AliceEmbedding.EmbeddingModel import AliceEmbedding

class AliceLongMemory:
    def __init__(self):
        """
        Initializes the object with default values for the `qdrant`, `embedding_model`, and `embedding_model_size` attributes.

        Parameters:
            None

        Returns:
            None
        """
        self.qdrant = None
        self.embedding_model = None
        self.embedding_model_size = None
        
    async def init_qdrant(self, qdrant_url: Optional[str] = "localhost", qdrant_port: Optional[int] = 6333):
        """
        Initializes the Qdrant client.

        Args:
            qdrant_url (Optional[str], optional): The URL of the Qdrant server. Defaults to "localhost".
            qdrant_port (Optional[int], optional): The port number of the Qdrant server. Defaults to 6333.

        Returns:
            None
        """
        self.qdrant = QdrantClient(host=qdrant_url, port=qdrant_port)
        
    async def init_embedding(self, embedding_model: Optional[str] = "all-minilm-l6-v2", size: Optional[int] = 384):
        """
        Initialize the embedding model with the specified parameters.

        Parameters:
            embedding_model (str): The name of the embedding model to initialize.
            size (int): The size of the embedding model.

        Returns:
            None
        """
        self.embedding_model = AliceEmbedding(embedding_model)
        self.embedding_model_size = size
        
    async def create_collection(self, collection_name: str):
        """
        Create a new collection with the specified name and associated vector configuration.

        :param collection_name: The name of the collection to be created.
        :type collection_name: str
        """
        self.qdrant.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=self.embedding_model_size, distance=Distance.COSINE),
        )
        
    async def insert_into_collection(self, collection_name: str, memory: dict):
        """
        Insert a memory into a collection if it does not already exist.

        Args:
            collection_name (str): The name of the collection.
            memory (dict): The memory to be inserted.

        Returns:
            None
        """
        # insert memory into collection if not exists
        points = self.qdrant.search(
            collection_name=collection_name,
            query_vector=self.embedding_model.embed(str(memory)),
            limit=1
        )
        if len(points) == 0: 
            id = str(uuid4())
            self.qdrant.upsert(
                collection_name=collection_name,
                points=[{"id": id, "vector": self.embedding_model.embed(str(memory)), "payload": memory}],
            )
        else:
            pass
    
    async def search_in_collection(self, collection_name: str, query: str, limit: Optional[int] = 5):
        """
        Searches for documents in a specified collection using a query string.

        Args:
            collection_name (str): The name of the collection to search in.
            query (str): The query string to search for.
            limit (Optional[int], optional): The maximum number of documents to return. Defaults to 5.

        Returns:
            The search results as a list of document IDs and their corresponding distances to the query vector.
        """
        return self.qdrant.search(
            collection_name=collection_name,
            query_vector=self.embedding_model.embed(query),
            limit=limit
        )
        
    async def delete_collection(self, collection_name: str):
        """
        Deletes a collection from the qdrant.

        :param collection_name: A string representing the name of the collection to be deleted.
        :type collection_name: str
        """
        self.qdrant.delete_collection(collection_name=collection_name)
        