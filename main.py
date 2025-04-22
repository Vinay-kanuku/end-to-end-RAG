import logging
from dotenv import load_dotenv
from src.pipeline.ingestion_pipeline import run_ingestion
from src.utils import format_documents
 
 

if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    
    try:
        vector_store = run_ingestion()
        while True:
            query = input("Enter your query: ")
            doc = vector_store.similarity_search(query)
            print(format_documents(doc))

    except Exception as e:
        logging.error("Error in ingestion pipeline", exc_info=True)
        print(f"❌ Pipeline error: {e}")

