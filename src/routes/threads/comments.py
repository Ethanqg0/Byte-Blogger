from src.routes.init_common_route import * #supabase and flask config
from src.services.posts_services import get_post

comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/posts/<int:post_id>/create_comment', methods=['POST'])
def create_comment(post_id):
    thread = get_post(post_id)
    if thread is None:
        return jsonify({'error': 'Post not found'}), 404
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        user = data.get('user')
        content = data.get('content')
        if not user or not content:
            return jsonify({'error': 'User and content are required'}), 400
        
        result = supabase.table('comments').insert({"content": content, "username": user, "parent_post_id": post_id}).execute()
        if result['status'] == 'error':
            return jsonify({'error': 'Failed to create comment'}), 500
        
        return jsonify({'message': 'Comment has been created'})

    except Exception as e:
        return jsonify({'error': 'Failed. Reason: Invalid data'}), 400
