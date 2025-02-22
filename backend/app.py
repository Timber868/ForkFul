from flask import Flask, g
from flask_cors import CORS
from blueprints.posts import posts
from blueprints.login import login_bp
from blueprints.users import users
from blueprints.recipes import recipes
from flask_login import LoginManager
from database.database import get_db

app = Flask(__name__)
app.secret_key = 'placeholder-key'
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])  

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login_bp.login'

@login_manager.user_loader
def load_user(user_id):
    connection = get_db()
    return User.get(connection, user_id)

app.register_blueprint(posts)
app.register_blueprint(login_bp)
app.register_blueprint(users)
app.register_blueprint(recipes)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/', methods=["GET"])
def home():
    return {"status": True}

if __name__ == '__main__':
    app.run(debug=True)