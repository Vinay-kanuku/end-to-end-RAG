from src.pipeline.ingestion_pipeline import run_ingestion
import google.generativeai as genai 
from src.constants import PROMPT_TEMPLATES, GEMINI_MODEL_NAME
from dotenv import load_dotenv
import os 
from  src.utils import format_documents
from abc import ABC, abstractmethod 
load_dotenv()
API_KEY = os.getenv("API_KEY")
genai.configure(api_key=API_KEY)


def run_gemini(prompt):
    model = genai.GenerativeModel(GEMINI_MODEL_NAME)
    response = model.generate_content(prompt)
    
    return response.text

if __name__ == "__main__":
    load_dotenv()
    ingestion = run_ingestion()
    doc = ingestion.similarity_search("What is the podcast about?")
 
    formated_doc = format_documents(doc)
     
    # use_case = input("Enter the use case (podcast_summary, science_explainer, code_analysis): ")
    prompt = PROMPT_TEMPLATES["podcast_summary"].format(context=formated_doc)
    print(prompt) 
    # print(run_gemini(prompt))
 





    

