import os
import click
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_caching import Cache

# Import configurations and models
from backend.config import Config
from backend.models.users import db, bcrypt, User
from backend.models.parking import ParkingLot, ParkingSpot, Booking

# Import blueprints
from backend.routes.auth_routes import auth_bp
from backend.routes.admin_routes import admin_bp
from backend.routes.user_routes import user_bp

# Global cache object
cache = Cache()

def create_app():
    """Application factory function."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # Create instance folder if not exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # --- Initialize Extensions ---
    db.init_app(app)
    bcrypt.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)
    CORS(app)  # Enable CORS for frontend integration

    # Initialize Cache (Redis by default from Config)
    cache.init_app(app)

    # --- Register Blueprints ---
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(user_bp, url_prefix='/api')

    # --- Simple health check route ---
    @app.route('/')
    def hello_world():
        return jsonify(message="Hello, World! The Parking System Backend is running. ✨"), 200

    # --- CLI command to initialize DB with admin user ---
    @app.cli.command("init-db")
    def init_db_command():
        """Creates the database tables and the initial admin user."""
        with app.app_context():
            db.create_all()
            
            # Check if admin already exists
            if User.query.filter_by(role='admin').first():
                click.echo('Admin user already exists.')
                return

            # Create the admin user
            admin_email = 'admin@parking.com'
            admin_password = 'adminpassword'  # Change for production
            admin_user = User(username='admin', email=admin_email, role='admin')
            admin_user.set_password(admin_password)
            
            db.session.add(admin_user)
            db.session.commit()
            
            click.echo('Initialized the database and created the admin user.')
            click.echo(f'Admin Email: {admin_email}')
            click.echo(f'Admin Password: {admin_password}')

    return app

# Example for setting FLASK_APP before running:
# PowerShell:
#   $env:FLASK_APP = "backend.app:create_app"
#   flask run
# Linux/Mac:
#   export FLASK_APP=backend.app:create_app
#   flask run
