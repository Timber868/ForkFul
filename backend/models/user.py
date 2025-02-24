from flask_login import UserMixin
from datetime import datetime

class User(UserMixin):
    def __init__(self, id, created, username, email, password, name, phoneNumber):
        self.username = username
        self.email = email
        self.password = password
        self.created = created
        self.name = name
        self.phoneNumber = phoneNumber
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
                row["password"],
                row["name"],
                row["phoneNumber"]
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
                row["password"],
                row["name"],
                row["phoneNumber"]
            )
        return None
    
    @classmethod
    def get_by_email(cls, db, email):
        cur = db.cursor()
        row = cur.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if row:
            return cls(
                row["id"],
                row["created"],
                row["username"],
                row["email"],
                row["password"],
                row["name"],
                row["phoneNumber"]
            )
        return None
    
    @classmethod
    def get_by_phoneNumber(cls, db, phoneNumber):
        cur = db.cursor()
        row = cur.execute("SELECT * FROM users WHERE phoneNumber = ?", (phoneNumber,)).fetchone()
        if row:
            return cls(
                row["id"],
                row["created"],
                row["username"],
                row["email"],
                row["password"],
                row["name"],
                row["phoneNumber"]
            )
        return None


    @staticmethod
    def create(db, username, email, password, name, phoneNumber):
        cur = db.cursor()
        cur.execute("INSERT INTO users (username, email, password, created, name, phoneNumber) VALUES (?, ?, ?, ?, ?, ?)", (username, email, password, datetime.now(), name, phoneNumber))
        db.commit()
        return User.get_by_username(db, username)
