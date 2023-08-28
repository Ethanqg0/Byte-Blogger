from config.supabase_config import * 
from src.services.threads import *
from flask import Flask, current_app, request, Blueprint, jsonify
from flask_cors import CORS, cross_origin
from src.services.authentication_services import is_a_user

threads_bp = Blueprint('threads', __name__)

@threads_bp.route('/create_thread', methods=['POST'])
@cross_origin()
def create_thread():
    data = request.get_json() 
    user = data['user']
    title = data['title']
    content = data['content']

    try:
        supabase.table('blog_posts').insert( {"title": title, "content": content, "username": user} ).execute()
        return 'good boy'
    except:
        return 'Failed. Reason: Invalid data'

    
@threads_bp.route('/threads/<thread_id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
def thread(thread_id):
    if request.method == 'GET':
        thread = get_thread(thread_id)
        return jsonify(thread)
    elif request.method == 'PUT':
        data = request.get_json()
        title = data['title']
        content = data['content']
        result = update_thread(thread_id, title, content)
        supabase.table('blog_posts').update({'title': title, 'content': content}).eq('post_id', thread_id).execute()

        return (f'Success! Thread {thread_id} has been updated')
    elif request.method == 'DELETE':
        result = delete_thread(thread_id)
        return result

@threads_bp.route('/threads', methods=['GET'])
@cross_origin()
def threads():
    threads = get_all_threads()
    return threads

@threads_bp.route('/add_like/<user>/<post_id>', methods=['GET'])
@cross_origin()
def add_like(user, post_id):
    result = update_post_likes(post_id, user)
    return result