from src.routes.init_common_route import * #supabase and flask confg
from src.services.posts_services import get_all_posts, get_post, get_post_by_user, update_post, delete_post, update_post_likes, remove_post_likes, is_a_user

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/posts', methods=['GET'])
def posts():
    posts = get_all_posts()
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
    posts = get_post_by_user(username)
    return posts

@posts_bp.route('/posts/<int:post_id>/like/<user>', methods=['POST', 'DELETE'])
def like_post(post_id, user):
    if request.method == 'POST':
        update_post_likes(post_id, user)
        return jsonify({'message': 'Like added'}), 200
    elif request.method == 'DELETE':
        remove_post_likes(post_id, user)
        return jsonify({'message': 'Like removed'}), 200
    else:
        return jsonify({'error': 'Invalid request'}), 400
    

""" # FIX ME
@posts_bp.route('/posts/create_post', methods=['POST'])
def create_post_route():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    user = data.get('user')
    title = data.get('title')
    content = data.get('content')

    if not is_a_user(user):
        return False, f'Failed. Reason: {user} is not a valid user'
    
    result = supabase.table('blog_posts').insert({"title": title, "content": content, "username": user}).execute()
    return 'success'
"""