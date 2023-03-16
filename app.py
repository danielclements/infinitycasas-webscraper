from flask import Flask, render_template, request, redirect, url_for
from bs4 import BeautifulSoup
import requests, random

app = Flask(__name__)



@app.route('/', methods=['POST', "GET"])
def index():
    if request.method == "POST":
        link_main = request.form["property-link"]
         # BeautifulSoup
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
            }
        html_text = requests.get(link_main, headers=headers).text
        soup = BeautifulSoup(html_text, 'lxml')

        # gets all images in the image gallery
        all_property_images = soup.find_all('a', class_='galleryItem')
        links_array = []
        for link in all_property_images:
            source = link.attrs['href']
            links_array.append(source)

        mainImage = links_array[0]
        image_top_row_r1 = links_array[random.randint(1, len(links_array))]
        image_top_row_r2 = links_array[random.randint(1, len(links_array))]
        image_bottom_row_r1 = links_array[random.randint(1, len(links_array))]
        image_bottom_row_r2 = links_array[random.randint(1, len(links_array))]
        image_bottom_row_r3 = links_array[random.randint(1, len(links_array))]


        # get property Header
        property_header = soup.find('h1', class_='pageTitle').text


        # get property Ref

        get_property_ref = soup.find('div', class_='additional').find_all('div', class_='amItem')
        property_ref = []
        for ref in get_property_ref:
            property_ref.append(ref.text.split()[-1])
        

        # get property Features

        property_features=soup.find('div', class_='amenities').find_all('div', class_='amItem')
        feature_array = []
        pool = "Communal Pool"
        for feature in property_features:
            feature_array.append(feature.text)

        # get property_description

        # property_description = soup.find('div', class_='entry-content').find('ul').find_all('li')
        property_description = soup.find('div', class_='entry-content').find_all('p')
        property_array = []

        for item in property_description:
            property_array.append(item.text)





        # get bedrooms and bathrooms

        beds = soup.find('ul', class_='features').find_all('li')[0].find('div').text[0]
        baths = soup.find('ul', class_='features').find_all('li')[1].find('div').text[0]


        # Get property price

        price = soup.find('div', class_='listPrice').find(text=True, recursive=False)

        
        return render_template(
            'print.html', property_header=property_header, price=price, beds=beds,
            baths=baths, pool=pool, property_ref=property_ref, mainImage=mainImage,
            image_top_row_r1=image_top_row_r1, image_top_row_r2=image_top_row_r2,
            image_bottom_row_r1=image_bottom_row_r1,
            image_bottom_row_r2=image_bottom_row_r2,
            image_bottom_row_r3=image_bottom_row_r3, property_array=property_array[0:9],
            links_array=links_array, feature_array=feature_array[0:9])
    else:
        return render_template(
        'index.html')


if __name__ == "__main__":
    app.run(debug=True)