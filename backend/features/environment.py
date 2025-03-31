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
        db.commit()