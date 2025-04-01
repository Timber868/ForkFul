from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from database.database import get_db
from models.user import User
from flask_cors import cross_origin

login_bp = Blueprint('login', __name__, url_prefix='/auth')

@login_bp.route('/login', methods=["POST"])
@cross_origin(supports_credentials=True)
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Please enter both email and password.'}), 400

    db = get_db()
    user = User.get_by_username(db, username)

    if user:
        if user.status == 'banned':
            return jsonify({'message': 'User is banned.'}), 403
        
        if check_password_hash(user.password, password):
            login_user(user)
            return jsonify({'message': 'Logged in successfully.'}), 200

    return jsonify({'message': 'Invalid username or password.'}), 401

@login_bp.route('/logout', methods=["POST"])
@cross_origin(supports_credentials=True)
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully.'}), 200

@login_bp.route('/current', methods=["GET"])
def current():
    if current_user.is_authenticated:
        return jsonify({
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email
        }), 200
    return jsonify({'message': 'No user is logged in.'}), 200
