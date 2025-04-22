
from langchain.text_splitter import RecursiveCharacterTextSplitter
from constants import CHUNK_SIZE, CHUNK_OVERLAP
class TextChunker:
    def __init__(self, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    def get_chunks(self, document):
        # Check if it's a Document object or a string
        if hasattr(document, 'page_content'):
            # It's a Document object, extract the text content
            return self.text_splitter.split_text(document.page_content)
        else:
            # It's already a string
            return self.text_splitter.split_text(document)
        

