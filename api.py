from flask import Flask
from src.routes.threads.posts import *
from src.routes.threads.comments import *
from src.routes.authentication.authentication import *
from config.supabase_config import * 

app = Flask(__name__)
CORS(app)

app.register_blueprint(posts_bp)
app.register_blueprint(comments_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5001"), debug=True)
