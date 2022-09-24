from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


# BeautifulSoup
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
html_text = requests.get('https://infinitycasas.com/properties/semi-detached-villa-in-cabo-roig/', headers=headers).text
soup = BeautifulSoup(html_text, 'lxml')

# gets all images in the image gallery
all_property_images = soup.find_all('a', class_='galleryItem')
links_array = []
for link in all_property_images:
    source = link.attrs['href']
    links_array.append(source)

mainImage = links_array[0]
image_top_row_r1 = links_array[11]
image_top_row_r2 = links_array[5]
image_bottom_row_r1 = links_array[17]
image_bottom_row_r2 = links_array[9]
image_bottom_row_r3 = links_array[7]


# get property Header
property_header = soup.find('h1', class_='pageTitle').text


# get property Ref

property_ref = soup.find('div', class_='additional').find_all('div', class_='amItem')[-1].text.split()[-1]

# get property Features

property_features=soup.find('div', class_='amenities').find_all('div', class_='amItem')
feature_array = []
pool = "Communal Pool"


# get property_description

property_description = soup.find('div', class_='entry-content').find('ul').find_all('li')
property_array = []

for item in property_description:
    property_array.append(item.text)





# get bedrooms oand bathrooms

beds = soup.find('ul', class_='features').find_all('li')[0].find('div').text[0]
baths = soup.find('ul', class_='features').find_all('li')[1].find('div').text[0]


# Get property price

price = soup.find('div', class_='listPrice').find(text=True, recursive=False)


@app.route('/')
def intial_load():
    
    
    return render_template(
        'index.html', property_header=property_header, price=price, beds=beds,
         baths=baths, pool=pool, property_ref=property_ref, mainImage=mainImage,
         image_top_row_r1=image_top_row_r1, image_top_row_r2=image_top_row_r2,
         image_bottom_row_r1=image_bottom_row_r1,
         image_bottom_row_r2=image_bottom_row_r2,
         image_bottom_row_r3=image_bottom_row_r3, property_array=property_array[0:9])


if __name__ == "__main__":
    app.run(debug=True)




