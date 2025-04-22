import logging
from src.utils import load_doc_using_langchain
from src.rag_db.chunking import TextChunker
from src.rag_db.embedding import Embedder
from src.rag_db.vectorstore import VectorStoreManager
from src.utils import format_documents
from src.constants import PROMPT_TEMPLATES

def run_ingestion(reset_db=False):
    logging.info("Starting document ingestion process")

    documents = load_doc_using_langchain()
    logging.info(f"Loaded {len(documents)} documents")

    chunker = TextChunker()
    embedder = Embedder()
    vector_store = VectorStoreManager(embedder)

    if reset_db:
        logging.info("Resetting the collection before ingestion")
        vector_store.reset_collection()

    total_chunks = 0
    for i, doc in enumerate(documents):
        logging.info(f"Processing document {i + 1}/{len(documents)}")

        chunks = chunker.get_chunks(doc)

        if chunks:
            vector_store.add(chunks)
            chunk_count = len(chunks)
            total_chunks += chunk_count
            logging.info(f"Added {chunk_count} chunks from document {i + 1}")

    logging.info(f"\u2705 Successfully added {total_chunks} chunks to the vector store.")
    return vector_store


if __name__ == "__main__":
    ingestion = run_ingestion(reset_db=False)
    doc = ingestion.similarity_search("What is the podcast about?")
 
    formated_doc = format_documents(doc)
     
    # use_case = input("Enter the use case (podcast_summary, science_explainer, code_analysis): ")
    prompt = PROMPT_TEMPLATES["podcast_summary"].format(context=formated_doc)
    print(prompt) 
    # print(run_gemini(prompt))