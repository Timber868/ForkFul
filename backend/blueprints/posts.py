from flask import Blueprint, jsonify, request
from database.database import get_db

posts = Blueprint('posts', __name__, url_prefix='/posts')

@posts.route('/', methods=["GET"])
def get_posts():
    cur = get_db().cursor()
    posts = cur.execute('SELECT * FROM posts').fetchall()
    return posts

@posts.route('/<int:post_id>', methods=["GET"])
def get_post(post_id):
    cur = get_db().cursor()
    post = cur.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()

    if post is None:
        return jsonify({"error": "Post not found"}), 404
    
    return post

@posts.route('/', methods=["POST"])
def create_post():
    data = request.get_json()
    db = get_db()
    cur = db.cursor()
    cur.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (data['title'], data['content']))

    # Check if the post was created
    post = cur.execute('SELECT * FROM posts WHERE id = ?', (cur.lastrowid,)).fetchone()
    if post is None:
        return jsonify({"error": "Post creation failed"}), 404
    
    db.commit()
    return post
