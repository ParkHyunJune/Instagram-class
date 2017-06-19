from django.core.exceptions import PermissionDenied
from post.models import Post

def post_owner(f)
    def wrap(request, *args, **kwargs):
        post = Post.objects.get(kwargs['post_pk'])
        if request.user == post.author:
            return function(request, *args, **kwargs)
        raise PermissionDenied
    return wrap
