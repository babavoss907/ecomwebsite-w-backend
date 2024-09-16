from flask import request, jsonify, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from .models import User  # Only import the User model


# Registration logic
def register_user():
    if request.method == "POST":
        from . import db  # Import db inside the function to avoid circular import

        data = request.form  # For HTML form data
        hashed_password = generate_password_hash(
            data["password"], method="pbkdf2:sha256"
        )
        new_user = User(
            username=data["username"],
            email=data["email"],
            password_hash=hashed_password,
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(
            url_for("login")
        )  # Redirect to login after successful registration
    return render_template("register.html")


# Login logic
def login_user():
    if request.method == "POST":
        from . import db  # Import db inside the function to avoid circular import

        data = request.form  # For HTML form data
        user = User.query.filter_by(email=data["email"]).first()
        if user and check_password_hash(user.password_hash, data["password"]):
            access_token = create_access_token(identity={"username": user.username})
            return redirect(
                url_for("index")
            )  # Redirect to the home page after successful login
        return jsonify({"message": "Invalid credentials!"}), 401
    return render_template("login.html")
