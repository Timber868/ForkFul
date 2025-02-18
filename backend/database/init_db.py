import sqlite3
from werkzeug.security import generate_password_hash

connection = sqlite3.connect('database/database.db')


with open('database/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Post', 'Content for the first post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post')
            )

hashed_password = generate_password_hash('password')

cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            ('admin', 'adming@gmail.com', hashed_password)
            )

connection.commit()
connection.close()