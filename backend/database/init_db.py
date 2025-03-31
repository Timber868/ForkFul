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

cur.execute("INSERT INTO users (username, email, password, name, phoneNumber, status) VALUES (?, ?, ?, ?, ?, ?)",
            ('admin', 'adming@gmail.com', hashed_password, 'Admin', '1234567890', 'active')
            )

cur.execute("INSERT INTO users (username, email, password, name, phoneNumber, status) VALUES (?, ?, ?, ?, ?, ?)",
            ('other', 'other@gmail.com', hashed_password, 'other', '1234567891', 'active'))

cur.execute("INSERT INTO users (username, email, password, name, phoneNumber, status) VALUES (?, ?, ?, ?, ?, ?)",
            ('empty', 'empty@gmail.com', hashed_password, 'empty', '1234567892', 'active'))

cur.execute('INSERT INTO recipes (name, posted_date, username, ingredients, description, image) VALUES (?, ?, ?, ?, ?, ?)',
                ('pasta', '12 January', 'admin', 'sauce, spaghetti', 'very yummy pasta', "../tests/test_image.jpg"))

cur.execute('INSERT INTO recipes (name, posted_date, username, ingredients, description, image) VALUES (?, ?, ?, ?, ?, ?)',
                ('pizza', '12 January', 'admin', 'cheese, pepperoni', 'very yummy pizza', "../tests/test_image.jpg"))

cur.execute('INSERT INTO recipes (name, posted_date, username, ingredients, description, image) VALUES (?, ?, ?, ?, ?, ?)',
                ('burger', '24 February', 'other', 'patty, bun, lettuce, ketchup, pickles, cheese', 'very yummy burger', "../tests/test_image.jpg"))

cur.execute('INSERT INTO reactions (user_id, recipe_id, reaction) VALUES (?, ?, ?)',
            (1, 1, 1))

cur.execute('INSERT INTO reactions (user_id, recipe_id, reaction) VALUES (?, ?, ?)',
            (1, 2, 0))

cur.execute('INSERT INTO reactions (user_id, recipe_id, reaction) VALUES (?, ?, ?)',
            (2, 1, 1))

cur.execute('INSERT INTO reactions (user_id, recipe_id, reaction) VALUES (?, ?, ?)',
            (2, 2, 1))

cur.execute('INSERT INTO reactions (user_id, recipe_id, reaction) VALUES (?, ?, ?)',
            (3, 1, 0))

cur.execute('INSERT INTO reactions (user_id, recipe_id, reaction) VALUES (?, ?, ?)',
            (3, 2, 0))

# cur.execute('INSERT INTO recipes (name, posted_date, username, ingredients, description, image) VALUES (?, ?, ?, ?, ?, ?)',
#                 (data['name'], data['posted_date'], data['username'], data['ingredients'], data['description'], filepath))

connection.commit()
connection.close()