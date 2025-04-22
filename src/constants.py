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
CHUNK_OVERLAP = 20

GEMINI_MODEL_NAME = "gemini-2.0-flash"


PROMPT_TEMPLATES = {
    "podcast_summary": """
You are a world-class summarization AI specialized in podcast transcripts. Your job is to transform long, unstructured dialogue into a **concise, high-signal summary** that reads like a podcast episode description from Spotify or Apple Podcasts.

🔧 TASK:
Summarize the transcript chunks below with:
- 🧠 Key insights and opinions from speakers
- 🎯 Actionable or memorable takeaways
- 🧑‍🤝‍🧑 Speaker names and their positions (if available)
- 📝 Keep it crisp, insightful, and engaging

--- TRANSCRIPT CHUNKS ---
{context}

📌 Output in 4–6 bullet points or a short paragraph. Avoid generic filler. Highlight unique angles.
""",

    "science_explainer": """
You are a senior science writer for a top publication like *Nature* or *Scientific American*.

🎯 Your goal is to **deconstruct and explain** the technical transcript below into **clear, accurate, accessible** explanations suitable for a college-educated non-expert.

TASK CHECKLIST:
- ✅ Break down jargon into understandable terms
- ✅ Retain important scientific accuracy
- ✅ Use analogies or examples where helpful

--- SCIENTIFIC TRANSCRIPT ---
{context}

📌 Return a clean, structured explanation in 2-3 short paragraphs. Avoid bullet points. Be natural, but precise.
""",

    "code_analysis": """
You are a senior software engineer reviewing a coding tutorial transcript.

🔍 Your job:
1. Explain what the code is doing
2. Identify best practices and pitfalls
3. Highlight architectural or performance considerations
4. Suggest improvements or simplifications if needed

--- CODE TUTORIAL TRANSCRIPT ---
{context}

📌 Structure output like this:
- 🧠 Summary of logic
- ✅ Best practices followed
- ⚠️ Issues or improvements
- 💡 Bonus tips (if applicable)

Use professional, concise, engineering-grade language.
"""
}