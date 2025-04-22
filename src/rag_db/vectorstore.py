import logging
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from constants import (
    QDRANT_HOST,
    QDRANT_PORT,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
)
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore

class VectorStoreManager:
    def __init__(
        self,
        embedder,
        host=QDRANT_HOST,
        port=6333,
        collection_name=COLLECTION_NAME,
    ):
        try:
            # Connect to REST API port
            self.client = QdrantClient(host=host, port=port)
            logging.info(f"Connected to Qdrant at {host}:{port}")
            
            # Test connection
            self.client.get_collections()
            logging.info("Successfully verified Qdrant connection")
        except Exception as e:
            logging.error(f"Failed to connect to Qdrant: {e}")
            raise
        
        # Check if collection exists and create if it doesn't
        try:
            if not self.client.collection_exists(collection_name):
                logging.info(f"Creating collection: {collection_name}")
                vector_size = 384  # Size for all-MiniLM-L6-v2
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(
                        size=vector_size, distance=Distance.COSINE
                    )
                )
                logging.info(f"Collection {collection_name} created successfully")
            else:
                logging.info(f"Collection {collection_name} already exists")
        except Exception as e:
            logging.error(f"Error working with collection: {e}")
            raise

        # Initialize QdrantVectorStore with correct parameters
        self.vectorstore = QdrantVectorStore(
            client=self.client,
            collection_name=collection_name,
            embedding=embedder.model,    
        )
        logging.info(f"Vector store initialized with collection '{collection_name}'")

    def add(self, chunks):
        if not chunks:
            logging.warning("No chunks provided to add to vector store")
            return None
        
        logging.info(f"Adding {len(chunks)} chunks to vector store")
        
        # Check if chunks are already Document objects
        if all(isinstance(chunk, Document) for chunk in chunks):
            # These are already Document objects
            return self.vectorstore.add_documents(chunks)
        else:
            # These are text strings, convert to Document objects
            docs = [Document(page_content=chunk) for chunk in chunks]
            return self.vectorstore.add_documents(docs)
        

    def similarity_search(self, query, k=5):
        return self.vectorstore.similarity_search(query, k=k)