from src.routes.init_common_route import *
from src.services.posts_services import *

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/posts', methods=['GET'])
def posts():
    posts = supabase.table('blog_posts').select("*").execute().data
    return posts

@posts_bp.route('/posts/<int:post_id>', methods=['GET', 'PUT', 'DELETE'])
def post(post_id):
    if request.method == 'GET':
        post = get_post(post_id)
        if post is None:
            return jsonify({'error': 'Post not found'}), 404
        return jsonify(post)
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        title = data.get('title')
        content = data.get('content')
        if title is None or content is None:
            return jsonify({'error': 'Title and content are required for updating'}), 400
        
        result = update_post(post_id, title, content)
        if not result:
            return jsonify({'error': 'Failed to update post'}), 500
        
        supabase.table('blog_posts').update({'title': title, 'content': content}).eq('post_id', post_id).execute()
        return jsonify({'message': f'Success! Thread {post_id} has been updated'})
    elif request.method == 'DELETE':
        result = delete_post(post_id)
        if not result:
            return jsonify({'error': 'Failed to delete post'}), 500
        return jsonify({'message': 'Post deleted successfully'})


@posts_bp.route('/posts/user/<username>', methods=['GET'])
def user_posts(username):
    threads = supabase.table('blog_posts').select("*").eq('username', username).execute().data
    return jsonify([thread for thread in threads if thread['parent_comment_id'] is None])

def create_post():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        user = data.get('user')
        title = data.get('title')
        content = data.get('content')

        if not user or not title or not content:
            return jsonify({'error': 'User, title, and content are required'}), 400
        
        # Assuming you have a valid supabase instance
        result = supabase.table('blog_posts').insert({"title": title, "content": content, "username": user}).execute()
        
        if result['status'] == 'error':
            return jsonify({'error': 'Failed to create post'}), 500
        
        return jsonify({'message': 'Success. Post has been created'})

    except Exception as e:
        return jsonify({'error': 'Failed. Reason: Invalid data'}), 400

    
@posts_bp.route('/add_like/<user>/<post_id>', methods=['GET'])
def add_like(user, post_id):
    result = update_post_likes(post_id, user)
    return result

@posts_bp.route('/remove_like/<user>/<post_id>', methods=['GET'])
def remove_like(user, post_id):
    result = remove_post_likes(post_id, user)
    return result