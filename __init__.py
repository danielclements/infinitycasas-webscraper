from flask import Flask
import os
from extensions import db, csrf, login_manager, proxy_fix
from routes import register_blueprints
from models import User
import auth  # This will register the user_loader

def create_app():
    app = Flask(__name__)

    # Security configurations
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['REMEMBER_COOKIE_SECURE'] = True
    app.config['REMEMBER_COOKIE_HTTPONLY'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    # Database configuration
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///properties.db')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    app.wsgi_app = proxy_fix(app.wsgi_app, x_proto=1, x_host=1)

    # Register blueprints
    register_blueprints(app)

    # Initialize database and create admin user if needed
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Create admin user if it doesn't exist
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', is_admin=True)
            admin.set_password(os.environ.get('ADMIN_PASSWORD', 'admin'))  # Change this in production!
            db.session.add(admin)
            db.session.commit()

    return app 