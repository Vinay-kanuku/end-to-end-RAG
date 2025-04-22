import logging
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from src.constants import QDRANT_HOST, COLLECTION_NAME
from src.utils import hash_text

class VectorStoreManager:
    def __init__(self, embedder, host=QDRANT_HOST, port=6333, collection_name=COLLECTION_NAME):
        self.collection_name = collection_name
        self.client = QdrantClient(host=host, port=port)

        logging.info(f"Connected to Qdrant at {host}:{port}")
        self._ensure_collection()

        self.vectorstore = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            embedding=embedder.model
        )
        logging.info(f"Vector store initialized with collection '{self.collection_name}'")

    def _ensure_collection(self):
        if not self.client.collection_exists(self.collection_name):
            logging.info(f"Creating collection: {self.collection_name}")
            self._create_collection()
        else:
            logging.info(f"Collection {self.collection_name} already exists")

    def _create_collection(self):
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=384,  # You can replace with a constant like EMBEDDING_DIM
                distance=Distance.COSINE
            )
        )
        logging.info(f"Collection {self.collection_name} created")

    def reset_collection(self):
        if self.client.collection_exists(self.collection_name):
            logging.info(f"Deleting existing collection: {self.collection_name}")
            self.client.delete_collection(self.collection_name)
        self._create_collection()

    def add(self, chunks):
        if not chunks:
            logging.warning("No chunks provided to add to vector store")
            return None

        logging.info(f"Adding {len(chunks)} chunks to vector store with deduplication")

        new_docs = []

        for chunk in chunks:
            content = chunk.page_content if isinstance(chunk, Document) else chunk
            chunk_hash = hash_text(content)

            existing = self.client.scroll(
                collection_name=self.collection_name,
                limit=1,
                with_payload=True,
                scroll_filter={
                    "must": [{"key": "hash", "match": {"value": chunk_hash}}]
                },
            )

            if not existing[0]:  # No match, safe to insert
                doc = Document(
                    page_content=content,
                    metadata={"hash": chunk_hash}
                )
                new_docs.append(doc)
            else:
                logging.info("Duplicate chunk detected — skipping insertion")

        if new_docs:
            return self.vectorstore.add_documents(new_docs)
        else:
            logging.info("No new documents to add (all were duplicates)")
            return None

    def similarity_search(self, query, k=5):
        return self.vectorstore.similarity_search(query, k=k)