 
import logging
from utils import load_doc_using_langchain
from rag_db.chunking import TextChunker
from rag_db.embedding import Embedder
from rag_db.vectorstore import VectorStoreManager
from constants import EMBEDDING_MODEL
from langchain_core.documents import Document


def run_ingestion():
    logging.info("Starting document ingestion process")

    documents = load_doc_using_langchain()
    logging.info(f"Loaded {len(documents)} documents")

    chunker = TextChunker()
    embedder = Embedder()
    vector_store = VectorStoreManager(embedder)

    total_chunks = 0
    for i, doc in enumerate(documents):
        logging.info(f"Processing document {i+1}/{len(documents)}")

        chunks = chunker.get_chunks(doc)
        doc_chunks = [Document(page_content=chunk) for chunk in chunks]

        if doc_chunks:
            vector_store.add(doc_chunks)
            chunk_count = len(doc_chunks)
            total_chunks += chunk_count
            logging.info(f"Added {chunk_count} chunks from document {i+1}")

    logging.info(f"✅ Successfully added {total_chunks} chunks to the vector store.")
    return vector_store