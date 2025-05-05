from flask import Blueprint, render_template, request, redirect, url_for, jsonify, abort, current_app
from flask_login import login_required
from models import Property
from extensions import db
from utils import is_valid_url, sanitize_url, extract_main_image
from datetime import datetime

properties_bp = Blueprint('properties', __name__)

@properties_bp.route('/window')
@login_required
def window():
    try:
        properties = Property.query.order_by(Property.position).all()
        return render_template('window.html', properties=properties)
    except Exception as e:
        current_app.logger.error(f"Error in window route: {str(e)}")
        abort(500)

@properties_bp.route('/add_property', methods=['GET', 'POST'])
@login_required
def add_property():
    if request.method == 'POST':
        try:
            link = request.form.get('property_link', '').strip()
            position = request.form.get('position', type=int)
            
            # Validate inputs
            if not link or not position or position < 1 or position > 30:
                abort(400, "Invalid input")
            
            if not is_valid_url(link):
                abort(400, "Invalid URL")
            
            # Sanitize the link
            link = sanitize_url(link)
            
            # Extract main image
            main_image = extract_main_image(link)
            
            # Check if position is already taken
            existing = Property.query.filter_by(position=position).first()
            if existing:
                existing.link = link
                existing.main_image = main_image
            else:
                new_property = Property(link=link, position=position, main_image=main_image)
                db.session.add(new_property)
            
            db.session.commit()
            return redirect(url_for('properties.window'))
        except Exception as e:
            current_app.logger.error(f"Error in add_property route: {str(e)}")
            db.session.rollback()
            abort(500)
    
    return render_template('add_property.html') 