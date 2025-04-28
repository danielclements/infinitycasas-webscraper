import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from flask import current_app

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def sanitize_url(url):
    # Remove any potentially dangerous characters
    return re.sub(r'[<>"\']', '', url)

def check_link_validity(link):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        
        # First try HEAD request
        try:
            response = requests.head(link, headers=headers, allow_redirects=True, timeout=10)
            if response.status_code < 400:
                return True
        except:
            pass  # If HEAD fails, try GET
            
        # If HEAD fails or returns error, try GET
        response = requests.get(link, headers=headers, allow_redirects=True, timeout=15, stream=True)
        return response.status_code < 400
    except Exception as e:
        current_app.logger.error(f"Error checking link validity for {link}: {str(e)}")
        return False

def extract_main_image(link):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        }
        html_text = requests.get(link, headers=headers, timeout=10).text
        soup = BeautifulSoup(html_text, 'lxml')
        
        # Try to find the main image
        main_image = soup.find('img', class_='img-fluid')
        if main_image and 'src' in main_image.attrs:
            return sanitize_url(main_image.attrs['src'])
        return None
    except:
        return None 