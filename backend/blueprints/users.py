from flask import Blueprint, jsonify, request
from database.database import get_db

users = Blueprint('users', __name__, url_prefix='/users')

@users.route('/', methods=["GET"])
def get_users():
    cur = get_db().cursor()
    users = cur.execute('SELECT * FROM users').fetchall()
    return jsonify(users)

@users.route('/<int:user_id>/ban', methods=['PUT'])
def ban_user(user_id):
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT status FROM users WHERE id = ?', (user_id,))
    user = cur.fetchone()
    
    if user and user['status'] == 'banned':
        return jsonify({"error": "User is already banned."}), 400

    cur.execute('UPDATE users SET status = ? WHERE id = ?', ('banned', user_id))
    db.commit()
    return jsonify({"message": f"User {user_id} has been banned."}), 200