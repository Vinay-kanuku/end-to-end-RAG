import streamlit as st
from src.pipeline.ingestion_pipeline import run_ingestion
from src.llms import run_gemini
from src.utils import format_documents
from src.constants import PROMPT_TEMPLATES
from src.get_knowledge import ContentExtractor, YouTubeExtractor, ArticleExtractor, PDFExtractor
import os
import logging
from pydantic import HttpUrl, ValidationError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize session state for query history
if "history" not in st.session_state:
    st.session_state.history = []

def validate_url(url: str) -> bool:
    """Validate if the input is a valid URL."""
    try:
        HttpUrl(url)
        return True
    except ValidationError:
        return False

def main():
    st.set_page_config(page_title="RAG Knowledge Base", page_icon="📚", layout="wide")
    st.title("📚 RAG Knowledge Base")

    # Sidebar for data ingestion
    st.sidebar.header("Ingest Data")
    source_type = st.sidebar.selectbox("Source Type", ["YouTube", "Article", "PDF"])
    source_input = st.sidebar.text_input("Enter URL or File Path")
    uploaded_file = None
    if source_type == "PDF":
        uploaded_file = st.sidebar.file_uploader("Upload PDF", type="pdf")

    if st.sidebar.button("Ingest"):
        if source_type == "PDF" and uploaded_file:
            try:
                # Save uploaded PDF temporarily
                temp_path = "temp.pdf"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                content_extractor = ContentExtractor(PDFExtractor())
                with st.spinner("Processing PDF..."):
                    content = content_extractor.process_source(temp_path)
                    os.remove(temp_path)  # Clean up
                if content:
                    st.success("PDF ingested successfully!")
                else:
                    st.error("Failed to extract content from PDF.")
            except Exception as e:
                st.error(f"Error processing PDF: {e}")
        elif source_input:
            # Validate URL for YouTube and Article sources
            if source_type in ["YouTube", "Article"] and not validate_url(source_input):
                st.error("Please provide a valid URL.")
                return
            try:
                extractor = {
                    "YouTube": YouTubeExtractor(),
                    "Article": ArticleExtractor(),
                    "PDF": PDFExtractor()
                }[source_type]
                content_extractor = ContentExtractor(extractor)
                with st.spinner(f"Processing {source_type}..."):
                    content = content_extractor.process_source(source_input)
                if content and "Error" not in content:
                    st.success(f"{source_type} ingested successfully!")
                else:
                    st.error(f"Failed to extract content: {content}")
            except Exception as e:
                st.error(f"Error processing {source_type}: {e}")
        else:
            st.error("Please provide a valid URL or upload a PDF.")

    # Main query section
    st.header("Query Knowledge Base")
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input("Enter your query", "What is the podcast about?")
    with col2:
        use_case = st.selectbox("Use Case", ["podcast_summary", "science_explainer", "code_analysis"])

    if st.button("Search"):
        if query:
            try:
                with st.spinner("Searching knowledge base..."):
                    vector_store = run_ingestion(reset_db=False)
                    docs = vector_store.similarity_search(query, k=5)
                    formatted_docs = format_documents(docs)
                    prompt = PROMPT_TEMPLATES[use_case].format(context=formatted_docs)
                    response = run_gemini(prompt)
                    st.markdown("### Response")
                    st.write(response)
                    # Save to history
                    st.session_state.history.append({"query": query, "use_case": use_case, "response": response})
            except Exception as e:
                st.error(f"Error querying knowledge base: {e}")
        else:
            st.error("Please enter a query.")

    # Query history
    if st.session_state.history:
        st.header("Query History")
        for i, item in enumerate(st.session_state.history[::-1]):  # Reverse to show latest first
            with st.expander(f"Query {len(st.session_state.history) - i}: {item['query']}"):
                st.write(f"**Use Case**: {item['use_case']}")
                st.write(f"**Response**: {item['response']}")

if __name__ == "__main__":
    main()  