MODEL_NAME = "gemini-1.5-flash"
DATA_DIR_NAME = "data/"
YOUTUBE_DATA_DIR_NAME = "youtube_data"
ARTICLE_DATA_DIR_NAME = "article_data"

QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
HOST_PORT = 6334
COLLECTION_NAME = "rag_docs"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 384
CHUNK_OVERLAP = 50


PROMPT_TEMPLATES = {
    "podcast_summary": """
You are a helpful AI assistant that summarizes long podcasts.
Summarize the following transcript chunks into a **crisp, engaging summary** that captures key points, guests’ opinions, and major takeaways.

TEXT:
{context}
""",

    "science_explainer": """
You are a research assistant helping simplify dense scientific content.
Explain the following transcript in clear, accessible language while retaining technical accuracy.

TEXT:
{context}
""",

    "code_analysis": """
You're a coding expert. Given the following transcript of a coding tutorial, explain what the code does, identify best practices, and summarize key implementation points.

TRANSCRIPT:
{context}
"""
}