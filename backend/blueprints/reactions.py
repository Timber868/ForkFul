from flask import Blueprint, jsonify, request
from database.database import get_db

reactions = Blueprint('reactions', __name__, url_prefix='/reactions')

@reactions.route('', methods=["GET"])
def get_reactions():

    user_id = request.args.get('user_id')
    recipe_id = request.args.get('recipe_id')

    if user_id is None and recipe_id is None:
        return jsonify({"error": "user_id and recipe_id is required"}), 400

    cur = get_db().cursor()
    reaction = cur.execute('SELECT "reaction" FROM reactions WHERE user_id = ? AND recipe_id = ?', (user_id, recipe_id)).fetchone()

    if reaction is not None:
        reaction = reaction["reaction"]

    count_booms = cur.execute('SELECT COUNT(*) FROM reactions WHERE recipe_id = ? AND reaction = 1', (recipe_id,)).fetchone()
    count_dooms = cur.execute('SELECT COUNT(*) FROM reactions WHERE recipe_id = ? AND reaction = 0', (recipe_id,)).fetchone()
    
    cur.close()

    return jsonify({
        "user_reaction": reaction,
        "booms": count_booms["COUNT(*)"],
        "dooms": count_dooms["COUNT(*)"]
    })


@reactions.route('', methods=["POST"])
def create_reaction():
    data = request.get_json()
    user_id = data.get('user_id')
    recipe_id = data.get('recipe_id')
    reaction = data.get('reaction')

    # Check if all required fields are present
    if user_id is None or recipe_id is None or reaction is None:
        return jsonify({"error": "user_id, recipe_id and reaction are required"}), 400
    
    # Check if the reaction is valid (0 or 1)
    if reaction not in [0, 1]:
        return jsonify({"error": "reaction must be 0 or 1"}), 400
    
    cur = get_db().cursor()

    # Check if a reaction already exists for the user and recipe
    existing_reaction = cur.execute('SELECT * FROM reactions WHERE user_id = ? AND recipe_id = ?', (user_id, recipe_id)).fetchone()
    if existing_reaction:
        # Update the existing reaction
        cur.execute('UPDATE reactions SET reaction = ? WHERE user_id = ? AND recipe_id = ?', (reaction, user_id, recipe_id))
    else:
        # Insert a new reaction
        cur.execute('INSERT INTO reactions (user_id, recipe_id, reaction) VALUES (?, ?, ?)',
                (user_id, recipe_id, reaction))
        
    get_db().commit()
    cur.close()

    return jsonify({"message": "Reaction added successfully"}), 201

@reactions.route('', methods=["DELETE"])
def delete_reaction():
    data = request.get_json()
    user_id = data.get('user_id')
    recipe_id = data.get('recipe_id')

    # Check if all required fields are present
    if user_id is None or recipe_id is None:
        return jsonify({"error": "user_id and recipe_id are required"}), 400
    
    cur = get_db().cursor()

    # Delete the reaction
    cur.execute('DELETE FROM reactions WHERE user_id = ? AND recipe_id = ?', (user_id, recipe_id))

    get_db().commit()
    cur.close()

    return jsonify({"message": "Reaction deleted successfully"}), 200
