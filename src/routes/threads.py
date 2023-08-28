from config.supabase_config import * 
from src.services.comments import *
from flask import Flask, current_app, request, Blueprint, jsonify
from flask_cors import CORS, cross_origin
from src.services.authentication_services import is_a_user

threads_bp = Blueprint('threads', __name__)

@threads_bp.route('/', methods=['GET'])
@cross_origin()
def index():
    return "API Currently running!"

@threads_bp.route('/threads', methods=['GET'])
@cross_origin()
def threads():
    if request.method == 'GET':
        threads = supabase.table('blog_posts').select("*").execute().data
        return jsonify([thread for thread in threads if thread['parent_comment_id'] is None])
    
@threads_bp.route('/threads/<thread_id>', methods=['GET', 'DELETE'])
@cross_origin()
def thread(thread_id):
    if request.method == 'GET':
        thread = supabase.table('blog_posts').select("*").eq('post_id', thread_id).execute().data
        return jsonify(thread)
    elif request.method == 'DELETE':
        supabase.table('blog_posts').delete().eq('post_id', thread_id).execute()
        return (f'Success! Thread {thread_id} has been deleted')

    




@threads_bp.route('/add_like/<user>/<post_id>', methods=['GET'])
@cross_origin()
def update_post_likes(post_id, user):
    likes = supabase.table('blog_posts').select("*").eq('post_id', post_id).execute().data[0]['likes']
    likes_from = supabase.table('blog_posts').select("*").eq('post_id', post_id).execute().data[0]['likes_from']

    if not is_a_user(user):
        return (f'Failed. Reason: {user} is not a valid user')

    if user not in likes_from:
        supabase.table('blog_posts').update({'likes': likes + 1}).eq('post_id', post_id).execute()
        supabase.table('blog_posts').update({'likes_from': likes_from + [user]}).eq('post_id', post_id).execute()
    else:
        return (f'Failed. Reason: {user} has already liked this post')

    return (f'Success! {user} has liked post {post_id} The likes have increased from {likes} to {likes + 1}')


if __name__ == "__main__":
    app.run(debug=True)