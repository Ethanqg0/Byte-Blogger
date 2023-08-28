from config.supabase_config import * 
from src.services.comments import *
from flask import Flask, current_app, request, Blueprint
from flask_cors import CORS, cross_origin

threads_bp = Blueprint('threads', __name__)

@threads_bp.route('/', methods=['GET'])
@cross_origin()
def index():
    return "Hello World! Test 2"

@threads_bp.route('/threads', methods=['GET'])
@cross_origin()
def threads():
    threads = supabase.table('blog_posts').select("*").execute().data
    return [thread for thread in threads if thread['parent_comment_id'] == None]

@threads_bp.route('/comments/<thread_id>', methods=['GET'])
@cross_origin()
def comments(thread_id):
    threads = supabase.table('blog_posts').select("*").execute().data
    return [thread for thread in threads if thread['parent_comment_id'] == thread_id]

@threads_bp.route('/threads', methods=['POST'])
@cross_origin()
def create_thread():
    data = request.get_json()
    supabase.table('blog_posts').insert([data]).execute()
    return 'OK'

@threads_bp.route('/update_comments_count', methods=['POST'])
@cross_origin()
def update_comments_count():
    data = request.get_json()
    return update_comments_count(data['username'], data['post_id'], data['comments_count'])


if __name__ == "__main__":
    app.run(debug=True)