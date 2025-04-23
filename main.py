import logging
from dotenv import load_dotenv
from src.pipeline.ingestion_pipeline import run_ingestion
from src.utils import format_documents
import os
from src.llms import run_gemini
from src.constants import PROMPT_TEMPLATES
os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)


if __name__ == "__main__":
    load_dotenv()
    ingestion = run_ingestion()
    querey = input("Enter your query: ")
    doc = ingestion.similarity_search(querey)
    formated_doc = format_documents(doc)
    prompt = PROMPT_TEMPLATES["podcast_summary"].format(context=formated_doc)
    print(run_gemini(prompt))

 

