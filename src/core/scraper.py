import requests
from bs4 import BeautifulSoup
import re
from config.config import HEADERS, REQUEST_TIMEOUT
from urllib.parse import urlparse

class WebScraper:
    def __init__(self):
        self.headers = HEADERS

    def scrape_website(self, url):
        """Scrape website content"""
        try:
            response = requests.get(
                url, 
                headers=self.headers, 
                timeout=REQUEST_TIMEOUT
            )
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract text content
            text_content = ' '.join([
                p.text for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'div'])
            ])
            text_content = re.sub(r'\s+', ' ', text_content).strip()
            
            # Extract metadata
            metadata = {
                'title': soup.title.text if soup.title else '',
                'meta_description': soup.find('meta', {'name': 'description'})['content'] if soup.find('meta', {'name': 'description'}) else ''
            }
            
            return {
                'content': text_content,
                'metadata': metadata
            }
            
        except Exception as e:
            raise Exception(f"Error scraping {url}: {str(e)}")
