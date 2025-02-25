from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from database.database import get_db
from models.user import User
from flask_cors import cross_origin

profile = Blueprint('profile', __name__, url_prefix='/profile')

@profile.route('/<username>', methods=["GET"])
def get_profile_info(username):
    cur = get_db().cursor()
    user = cur.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

    if user is None:
        return jsonify({"message": "This profile does not exist or is no longer available."}), 404
    

    recipes = cur.execute('SELECT * FROM recipes WHERE username = ?', (username,)).fetchall()

    if len(recipes) == 0:
        message = "No recipes posted yet."
    else:
        message = "Profile exists with recipes!"

    cur.close()

    return jsonify({
        "user": {
            "id": user["id"],
            "created": user["created"],
            "username": user["username"],
            "email": user["email"],
            "phoneNumber": user["phoneNumber"],
            "name": user["name"]
        },
        "recipes": [{
            "id": recipe["id"],
            "created": recipe["created"],
            "name": recipe["name"],
            "posted_date": recipe["posted_date"],
            "username": recipe["username"],
            "ingredients": recipe["ingredients"],
            "description": recipe["description"],
            "image": recipe["image"]
        } for recipe in recipes],
        "message" : message
    })

