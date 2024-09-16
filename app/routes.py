from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import User


def protected_route():
    current_user = get_jwt_identity()
    return jsonify({"logged_in_as": current_user})


def get_users():
    users = User.query.all()
    return jsonify([{"username": user.username, "email": user.email} for user in users])
