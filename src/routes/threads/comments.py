from src.routes.init_common_route import *
from src.services.threads import *
from src.services.authentication_services import is_a_user

comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/posts/<post_id>/create_comment', methods=['POST'])
@cross_origin()
def create_comment(post_id):
    thread = get_thread(post_id)
    data = request.get_json()
    user = data['user']
    content = data['content']
    try:
        supabase.table('blog_posts').insert( {"content": content, "username": user, "parent_comment_id": post_id} ).execute()
    except:
        return 'Failed. Reason: Invalid data'