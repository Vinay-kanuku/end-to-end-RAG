import logging
import pdfplumber 
import os 
from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup 
import re
from youtube_transcript_api import YouTubeTranscriptApi
from typing import Optional
from src.config import YoutubeConfig, ArticleConfig
from datetime import datetime
 
class KnowledgeBase(ABC):
    """Abstract base class for all data extraction implementations."""
    
    @abstractmethod
    def extract_data(self, source_path: str) -> str:
        """Extract data from the given source path.
        
        Args:
            source_path: Path or URL to the source
            
        Returns:
            Extracted content as string
        """
        pass
    
    def save_data(self, data: str, file_path: str) -> bool:
        """Save extracted data to a file.
        
        Args:
            data: Content to save
            file_path: Path where to save the content
            
        Returns:
            True if successful, False otherwise
        """
    
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(data)
            return True
        except Exception as e:
            logging.error(f"Error saving data to file: {e}")
            return False
    
    def process_source(self, source_path: str, output_path: str) -> str:
        """Process a source by extracting data and saving it.
        
        Args:
            source_path: Path or URL to the source
            output_path: Path where to save the extracted content
            
        Returns:
            Extracted content
        """
        data = self.extract_data(source_path)
        if data:
            self.save_data(data, output_path)
        return data

class PDFExtractor(KnowledgeBase):
    """Extract text content from PDF files."""
    name = "pdf"
    
    def extract_data(self, source_path: str) -> str:
        try:
            with pdfplumber.open(source_path) as pdf:
                text = ""
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted
                return text
        except FileNotFoundError as e:
            logging.error(f"PDF file not found: {source_path}. Error: {e}")
            return ""
        except Exception as e:
            logging.error(f"Error extracting data from PDF: {e}")
            return ""

class ArticleExtractor(KnowledgeBase):
    """Extract content from web articles."""
    name = "article"
    
    def extract_data(self, source_path: str) -> str:
        """Extract text from a web article.
        
        Args:
            source_path: URL of the article
            
        Returns:
            Extracted article text
        """
        return self._fetch_text_from_web(source_path)
    
    def _fetch_text_from_web(self, url: str) -> str:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                element.decompose()

            if 'wikipedia.org' in url:
                for element in soup.find_all(class_=['reflist', 'navbox', 'mw-editsection']):
                    element.decompose()
                # Remove specific sections
                for section in soup.find_all(['h2', 'h3']):
                    if section.text.lower() in ['references', 'external links', 'see also', 'further reading']:
                        next_sibling = section.find_next_sibling()
                        while next_sibling and next_sibling.name not in ['h2', 'h3']:
                            next_sibling.decompose()
                            next_sibling = section.find_next_sibling()

            # Extract text from relevant elements
            elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'li'])
            text_parts = []
            for element in elements:
                text = element.get_text(strip=True)
                if text and len(text) > 20:  # Ignore very short snippets
                    text_parts.append(text)

            text = ' '.join(text_parts)
            text = re.sub(r'\s+', ' ', text).strip()   
            return text[:10000] if text else "No content extracted"
        except Exception as e:
            logging.error(f"Error extracting article: {str(e)}")
            return f"Error extracting article: {str(e)}"

class YouTubeExtractor(KnowledgeBase):
    """Extract transcript from YouTube videos."""
    name = "youtube"
    
    def extract_data(self, source_path: str) -> str:
        """Extract transcript from a YouTube video.
        
        Args:
            source_path: URL of the YouTube video
            
        Returns:
            Extracted transcript text
        """
        return self._fetch_text_from_youtube(source_path)

    def _extract_video_id(self, url: str) -> str:
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        raise ValueError("Could not extract video ID from URL")

    def _fetch_text_from_youtube(self, url: str) -> str:
        try:
            if not any(domain in url.lower() for domain in ['youtube.com', 'youtu.be']):
                raise ValueError("Invalid YouTube URL")

            video_id = self._extract_video_id(url)
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            
            # Process and clean the transcript
            text_parts = []
            for segment in transcript_list:
                text = segment.get('text', '').strip()
                if text:
                    text_parts.append(text)

            cleaned_text = ' '.join(text_parts)
            # Remove multiple spaces and normalize whitespace
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
            
            return cleaned_text if cleaned_text else "No transcript available"

        except ValueError as e:
            logging.error(f"URL validation error: {str(e)}")
            return f"URL validation error: {str(e)}"
        except Exception as e:
            logging.error(f"Error extracting YouTube transcript: {str(e)}")
            return f"Error extracting YouTube transcript: {str(e)}"

class ContentExtractor:
    """Factory class to work with different extractor types."""
    
    def __init__(self, extractor: KnowledgeBase):
        self.extractor = extractor 
    
    def extract_data(self, source_path: str) -> str:
        return self.extractor.extract_data(source_path)
    
    def process_source(self, source_path: str) -> str:
        if self.extractor.name == "youtube":
            os.makedirs(YoutubeConfig().data_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(YoutubeConfig().data_dir, f"youtube_{timestamp}.txt")
        elif self.extractor.name == "article":
            os.makedirs(ArticleConfig().data_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(ArticleConfig().data_dir, f"article_{timestamp}.txt")
        return self.extractor.process_source(source_path, output_path)

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    y_extractor = YouTubeExtractor()
    a_extractor = ArticleExtractor()
    ob = ContentExtractor(y_extractor)
    url = input("Enter the URL: ")
    ob.process_source(url)
    
  