from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from redis import Redis
from .models import User  # Import your User model
from .auth import register_user, login_user  # Import auth functions

# Initialize the extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
redis_client = Redis(host="localhost", port=6379)


def create_app():
    app = Flask(__name__)

    # Load configurations from config.py
    app.config.from_object("config.Config")

    # Initialize the extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Route for the registration page (calls logic in auth.py)
    @app.route("/register", methods=["GET", "POST"])
    def register():
        return register_user()  # Logic is in auth.py

    # Route for the login page (calls logic in auth.py)
    @app.route("/login", methods=["GET", "POST"])
    def login():
        return login_user()  # Logic is in auth.py

    # Protected route example (JWT-protected)
    @app.route("/protected", methods=["GET"])
    @jwt_required()  # Requires JWT token to access
    def protected():
        current_user = get_jwt_identity()
        return jsonify({"logged_in_as": current_user})

    # Home route (optional - renders index.html)
    @app.route("/")
    def index():
        return render_template("index.html")

    # Return the Flask app instance
    return app
