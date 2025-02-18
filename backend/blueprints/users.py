from flask import Blueprint, jsonify, request
from database.database import get_db

users = Blueprint('users', __name__, url_prefix='/users')

@users.route('/', methods=["GET"])
def get_users():
    cur = get_db().cursor()
    users = cur.execute('SELECT * FROM users').fetchall()
    return jsonify(users)