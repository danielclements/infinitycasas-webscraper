from flask import Blueprint, render_template, request, abort, redirect, url_for
from flask_login import login_required, current_user
from bs4 import BeautifulSoup
import requests
import random

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
        
    if request.method == "POST":
        link_main = request.form["property-link"]
        # BeautifulSoup
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        }
        html_text = requests.get(link_main, headers=headers).text
        soup = BeautifulSoup(html_text, 'lxml')

        # gets all images in the image gallery
        all_property_images = soup.find_all('img', class_='img-fluid')
        links_array = []
        for link in all_property_images:
            source = link.attrs['src']
            links_array.append(source)

        mainImage = links_array[0]
        image_top_row_r1 = links_array[random.randint(1, len(links_array))]
        image_top_row_r2 = links_array[random.randint(1, len(links_array))]
        image_bottom_row_r1 = links_array[random.randint(1, len(links_array))]
        image_bottom_row_r2 = links_array[random.randint(1, len(links_array))]
        image_bottom_row_r3 = links_array[random.randint(1, len(links_array))]

        # get property Header
        property_header = soup.find('li', class_='breadcrumb-item active').text

        # get property Ref
        get_property_ref = soup.find_all('li', class_='property-overview-item')
        property_ref = []
        for ref in get_property_ref:
            property_ref.append(ref.text.split()[-1])

        # get property Features
        property_features=soup.find('div', class_='property-features-wrap').find('div').find('div', class_='block-content-wrap').find('ul').find_all('li')
        feature_array = []
        pool = "Communal Pool"
        for feature in property_features:
            feature_array.append(feature.text)

        # get bedrooms and bathrooms
        beds = soup.find('i', class_='houzez-icon icon-hotel-double-bed-1 mr-1').next_sibling.next_sibling.text
        baths = soup.find('i', class_='icon-bathroom-shower-1').next_sibling.next_sibling.text

        # Get property price
        price = soup.find('li', class_='item-price').find(text=True, recursive=False)
        
        return render_template(
            'print.html', property_header=property_header, property_ref=property_ref, beds=beds,
            baths=baths, feature_array=feature_array[0:9], pool=pool, mainImage=mainImage,
            image_top_row_r1=image_top_row_r1, image_top_row_r2=image_top_row_r2,
            image_bottom_row_r1=image_bottom_row_r1,
            image_bottom_row_r2=image_bottom_row_r2,
            image_bottom_row_r3=image_bottom_row_r3,
            links_array=links_array, price=price)
    else:
        return render_template('home.html')

@main_bp.errorhandler(400)
def bad_request(error):
    return render_template('error.html', error="Invalid request"), 400

@main_bp.errorhandler(500)
def server_error(error):
    return render_template('error.html', error="Server error"), 500 