from flask import Flask, g
from flask_cors import CORS
from blueprints.posts import posts

app = Flask(__name__)
CORS(app)

app.register_blueprint(posts)

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