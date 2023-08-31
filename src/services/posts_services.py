from config.supabase_config import * 
from src.services.authentication_services import *
from flask import jsonify

def get_all_posts():
    posts = supabase.table('blog_posts').select("*").execute().data
    return jsonify([post for post in posts if post['parent_comment_id'] is None])

def get_post(post_id):
    post = supabase.table('blog_posts').select("*").eq('post_id', post_id).execute().data
    return post

def get_post_by_user(username):
    threads = supabase.table('blog_posts').select("*").eq('username', username).execute().data
    return jsonify([thread for thread in threads if thread['parent_comment_id'] is None])

"""
                                    I broken
def create_post(user, title, content):
    if not is_a_user(user):
        return False, f'Failed. Reason: {user} is not a valid user'

    # Get the last index from the blog_posts table
    last_index = supabase.table('blog_posts').select('index', order_by='index.desc', limit=1).execute().data[0]['index']
    
    new_index = int(last_index + 1)
    
    result = supabase.table('blog_posts').insert({"title": title, "content": content, "username": user}).execute()

    if result['status'] == 'error':
        return False, 'Failed to create post'  

    return True, f'Success! Post {title} has been created'
"""


def update_post(post_id, title, content):
    supabase.table('blog_posts').update({'title': title, 'content': content}).eq('post_id', post_id).execute()

def delete_post(post_id):
    supabase.table('blog_posts').delete().eq('post_id', post_id).execute()
    return f'Success! Post {post_id} has been deleted'

def update_post_likes(post_id, user):
    likes = supabase.table('blog_posts').select("*").eq('post_id', post_id).execute().data[0]['likes']
    likes_from = supabase.table('blog_posts').select("*").eq('post_id', post_id).execute().data[0]['likes_from']

    if not is_a_user(user):
        return f'Failed. Reason: {user} is not a valid user'

    if user not in likes_from:
        supabase.table('blog_posts').update({'likes': likes + 1}).eq('post_id', post_id).execute()
        supabase.table('blog_posts').update({'likes_from': likes_from + [user]}).eq('post_id', post_id).execute()
    else:
        return f'Failed. Reason: {user} has already liked this post'

    return f'Success! {user} has liked post {post_id}. The likes have increased from {likes} to {likes + 1}'

def remove_post_likes(post_id, user):
    likes = supabase.table('blog_posts').select("*").eq('post_id', post_id).execute().data[0]['likes']
    likes_from = supabase.table('blog_posts').select("*").eq('post_id', post_id).execute().data[0]['likes_from']

    if not is_a_user(user):
        return f'Failed. Reason: {user} is not a valid user'

    if user in likes_from:
        supabase.table('blog_posts').update({'likes': likes - 1}).eq('post_id', post_id).execute()
        supabase.table('blog_posts').update({'likes_from': [user for user in likes_from if user != user]}).eq('post_id', post_id).execute()
    else:
        return f'Failed. Reason: {user} has not liked this post'

    return f'Success! {user} has unliked post {post_id}. The likes have decreased from {likes} to {likes - 1}'