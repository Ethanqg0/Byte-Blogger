from flask import Flask
from src.routes.threads import threads_bp
from src.routes.authentication import auth_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(threads_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run()