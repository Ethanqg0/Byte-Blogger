from config.supabase_config import * 
from flask import Flask, current_app, request
from flask_cors import CORS, cross_origin
import requests

app = Flask(__name__)
CORS(app)

def update_comments_count(username, post_id, comments_count):
    api_url = f"https://fnubpfmungeeuslnosxe.supabase.co/rest/v1/blog_posts?post_id=eq.{post_id}"

    supabase_key = os.environ.get('API_KEY')

    data = {
        "comments_count": comments_count + 1    
    }

    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    response = requests.patch(api_url, json=data, headers=headers)

    if response.status_code == 200:
        return "Likes updated successfully"
    else:
        return "Failed to update likes"
    


def update_post_likes(username, post_id, likes, likes_from):
    # Supabase API URL
    api_url = f"https://fnubpfmungeeuslnosxe.supabase.co/rest/v1/blog_posts?post_id=eq.{post_id}"

    # Supabase API key
    supabase_key = os.environ.get('API_KEY')

    updated_likes_from = likes_from + [username]
    # Update data
    data = {
        "likes": likes + 1,
        "likes_from": updated_likes_from
    }

    # Headers
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    # Send the update request using requests
    response = requests.patch(api_url, json=data, headers=headers)

    if response.status_code == 200:
        return "Likes updated successfully"
    else:
        return "Failed to update likes"