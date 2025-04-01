from flask import Flask
from database.database import get_db
from werkzeug.security import generate_password_hash

from app import app

hashed_password = generate_password_hash('password')

def before_feature(context, feature):
    context.app = app
    context.client = context.app.test_client()

    with context.app.app_context():
        db = get_db()
        # Either delete existing rows:
        db.execute("DELETE FROM users")
        db.execute("INSERT INTO users (username, email, password, name, phoneNumber, status) VALUES (?, ?, ?, ?, ?, ?)",
            ('admin', 'adming@gmail.com', hashed_password, 'Admin', '1234567890', 'active')
            )
        db.commit()

def before_scenario(context, scenario):
    """
    This hook runs before *each* scenario and resets the `users` table
    so there's no leftover data from any previous scenario.
    """
    context.app = app
    context.client = context.app.test_client()

    with context.app.app_context():
        db = get_db()
        # Either delete existing rows:
        db.execute("DELETE FROM users")
        db.execute("INSERT INTO users (username, email, password, name, phoneNumber, status) VALUES (?, ?, ?, ?, ?, ?)",
            ('admin', 'adming@gmail.com', hashed_password, 'Admin', '1234567890', 'active')
            )
        db.execute("INSERT INTO users (username, email, password, name, phoneNumber, status) VALUES (?, ?, ?, ?, ?, ?)",
            ('other', 'other@gmail.com', hashed_password, 'other', '1234567891', 'active'))

        db.execute("INSERT INTO users (username, email, password, name, phoneNumber, status) VALUES (?, ?, ?, ?, ?, ?)",
            ('empty', 'empty@gmail.com', hashed_password, 'empty', '1234567892', 'active'))

        # Add the test recipe with reactions
        db.execute("DELETE FROM recipes WHERE name = ?", ('Test Recipe Reactions',))
        db.execute('INSERT INTO recipes (name, posted_date, username, ingredients, description, image) VALUES (?, ?, ?, ?, ?, ?)',
                ('Test Recipe Reactions', '31 March', 'admin', 'chili, beans', 'very yummy chili', "../tests/test_image.jpg"))
        # Get the recipe ID of the newly inserted recipe
        recipe_id = db.execute('SELECT id FROM recipes WHERE name = ?', ('Test Recipe Reactions',)).fetchone()['id']
        # Add reactions to the recipe
        db.execute('INSERT INTO reactions (user_id, recipe_id, reaction) VALUES (?, ?, ?)',
                (1, recipe_id, 1))
        db.execute('INSERT INTO reactions (user_id, recipe_id, reaction) VALUES (?, ?, ?)',
                (2, recipe_id, 0))
        db.execute('INSERT INTO reactions (user_id, recipe_id, reaction) VALUES (?, ?, ?)',
                (3, recipe_id, 1))
        
        db.commit()