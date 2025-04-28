from flask import Blueprint, render_template, request, redirect, url_for, jsonify, abort, current_app
from flask_login import login_required
from models import Property
from extensions import db
from utils import is_valid_url, sanitize_url, check_link_validity, extract_main_image
from datetime import datetime, timedelta

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

@properties_bp.route('/check_links')
@login_required
def check_links():
    try:
        properties = Property.query.all()
        results = {}
        now = datetime.utcnow()
        recheck_threshold = now - timedelta(hours=24)  # Only recheck after 24 hours
        
        for property in properties:
            # Skip rechecking if the link was already marked as invalid and checked recently
            if not property.is_valid and property.last_checked and property.last_checked > recheck_threshold:
                if property.consecutive_fails >= 3:  # If failed 3 times in a row, don't check for a week
                    if property.last_checked > now - timedelta(days=7):
                        results[property.position] = False
                        continue
                else:
                    results[property.position] = False
                    continue
            
            is_valid = check_link_validity(property.link)
            property.is_valid = is_valid
            property.last_checked = now
            
            if not is_valid:
                property.consecutive_fails += 1
            else:
                property.consecutive_fails = 0
                
            results[property.position] = is_valid
            
        db.session.commit()
        return jsonify(results)
    except Exception as e:
        current_app.logger.error(f"Error checking links: {str(e)}")
        return jsonify({'error': str(e)}), 500

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
            
            # Sanitize and validate the link
            link = sanitize_url(link)
            
            # Extract main image and check link validity
            main_image = extract_main_image(link)
            is_valid = check_link_validity(link)
            
            # Check if position is already taken
            existing = Property.query.filter_by(position=position).first()
            if existing:
                existing.link = link
                existing.main_image = main_image
                existing.is_valid = is_valid
            else:
                new_property = Property(link=link, position=position, main_image=main_image, is_valid=is_valid)
                db.session.add(new_property)
            
            db.session.commit()
            return redirect(url_for('properties.window'))
        except Exception as e:
            current_app.logger.error(f"Error in add_property route: {str(e)}")
            db.session.rollback()
            abort(500)
    
    return render_template('add_property.html') 