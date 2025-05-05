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