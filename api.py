from flask import Flask
from src.routes.threads.posts import *
from src.routes.threads.comments import *
from src.routes.authentication.authentication import *
from config.supabase_config import * 
from flask_caching import Cache

app = Flask(__name__)

# Set up Memcached configuration
app.config['CACHE_TYPE'] = 'memcached'
app.config['CACHE_MEMCACHED_SERVERS'] = ['127.0.0.1:5000']
cache = Cache(app)

app.register_blueprint(posts_bp)
app.register_blueprint(comments_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run()
