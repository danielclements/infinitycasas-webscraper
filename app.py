from flask import Flask
from bs4 import BeautifulSoup
import requests


def intial_load():
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }

    html_text = requests.get('https://infinitycasas.com/properties/cbw-474752-villa-in-torre-de-la-horadada/', headers=headers).text
    soup = BeautifulSoup(html_text, 'lxml')
    all_property_images = soup.find_all('a', class_='galleryItem')
    for link in all_property_images.find_all('img'):
        print(link.get('image-src'))
    

    
    return all_property_images



