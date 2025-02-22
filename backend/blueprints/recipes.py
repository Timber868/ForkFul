import os
import re
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from database.database import get_db

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

recipes = Blueprint('recipes', __name__, url_prefix='/recipes')

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_valid_date(date_string):
    """Validate date format (YYYY-MM-DD)"""
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", date_string))

@recipes.route('/', methods=["POST"])
def create_recipe():
    """Create a new recipe with text and image validation"""
    
    # Expecting form-data instead of JSON
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    data = request.form  # Use form-data instead of request.get_json()

    # Validate required fields
    required_fields = ["name", "posted_date", "username", "ingredients", "description"]
    for field in required_fields:
        if field not in data or not data[field].strip():
            return jsonify({"error": f"{field} is required and cannot be empty"}), 400

    # Validate date format
    if not is_valid_date(data["posted_date"]):
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    # Validate image
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Allowed types: png, jpg, jpeg, gif"}), 400

    # Save the image
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    db = get_db()
    cur = db.cursor()

    cur.execute('INSERT INTO recipes (name, posted_date, username, ingredients, description, image) VALUES (?, ?, ?, ?, ?, ?)',
                (data['name'], data['posted_date'], data['username'], data['ingredients'], data['description'], filepath))

    db.commit()

    # Retrieve the newly created recipe
    recipe = cur.execute('SELECT * FROM recipes WHERE id = ?', (cur.lastrowid,)).fetchone()

    if recipe is None:
        return jsonify({"error": "Recipe creation failed"}), 400

    return jsonify({"message": "Recipe successfully created!", "recipe": recipe}), 201

@recipes.route('/', methods=["GET"])
def get_recipes():
    """Retrieve all recipes"""
    cur = get_db().cursor()
    recipes = cur.execute('SELECT * FROM recipes').fetchall()
    return jsonify(recipes), 200


