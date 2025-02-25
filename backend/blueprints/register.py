from flask import Blueprint, request, jsonify
from database.database import get_db
from models.user import User
from flask_cors import cross_origin
from werkzeug.security import generate_password_hash

register_bp = Blueprint('register', __name__, url_prefix='/auth')

@register_bp.route('/register', methods=["POST"])
@cross_origin(origins="http://localhost:5173", supports_credentials=True)
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    phoneNumber = data.get('phoneNumber')

    if not username or not email or not password or not name or not phoneNumber:
        return jsonify({'message': 'Please enter all fields.'}), 400

    db = get_db()
    user = User.get_by_username(db, username)
    if user:
        return jsonify({'message': 'Username already exists.'}), 400

    user = User.get_by_email(db, email)
    if user:
        return jsonify({'message': 'Email already exists.'}), 400
    
    user = User.get_by_phoneNumber(db, phoneNumber)
    if user:
        return jsonify({'message': 'Phone number already exists.'}), 400

    # hash password
    hashed_password = generate_password_hash(password)

    user = User.create(db, username, email, hashed_password, name, phoneNumber)
    return jsonify({'message': 'User created successfully.'}), 200
