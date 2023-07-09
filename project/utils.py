from werkzeug.exceptions import abort
from .models import Post

def get_post(post_id):
    post = Post.query.filter(Post.id == post_id).first()
    if post is None:
        abort(404)
    return post