from config.supabase_config import * 
from services.comments import *
from flask import Flask, current_app, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

# Access app configurations directly
app_name = app.name
debug_mode = app.debug

@app.route('/', methods=['GET'])
@cross_origin()
def index():
    return "Hello World! Test 2"

@app.route('/threads', methods=['GET'])
@cross_origin()
def threads():
    threads = supabase.table('blog_posts').select("*").execute().data
    return [thread for thread in threads if thread['parent_comment_id'] == None]

@app.route('/comments/<thread_id>', methods=['GET'])
@cross_origin()
def comments(thread_id):
    threads = supabase.table('blog_posts').select("*").execute().data
    return [thread for thread in threads if thread['parent_comment_id'] == thread_id]

@app.route('/threads', methods=['POST'])
@cross_origin()
def create_thread():
    data = request.get_json()
    supabase.table('blog_posts').insert([data]).execute()
    return 'OK'

@app.route('/update_comments_count', methods=['POST'])
@cross_origin()
def update_comments_count():
    data = request.get_json()
    return update_comments_count(data['username'], data['post_id'], data['comments_count'])


if __name__ == "__main__":
    app.run(debug=True)