from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, created, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.created = created
        self.id = id

    @classmethod
    def get(cls, db, user_id):
        cur = db.cursor()
        row = cur.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if row:
            # Manually extract values using the dictionary keys
            return cls(
                row["id"],
                row["created"],
                row["username"],
                row["email"],
                row["password"]
            )
        return None

    @classmethod
    def get_by_username(cls, db, username):
        cur = db.cursor()
        row = cur.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if row:
            return cls(
                row["id"],
                row["created"],
                row["username"],
                row["email"],
                row["password"]
            )
        return None
