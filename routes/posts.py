from flask_restful import Resource
from models.post import Post
from helpers.auth import (
    security
)


def _needs_post(post_owner_only=False):
    """
    Abstraction decorator for endpoints that need a post to be
    useful
    """
    def decorator(function):
        def wrapper(*args, **kwargs):
            kwargs["post"] = Post.query.filter(
                Post.slug == kwargs["post_slug"]).first()

            # NOTE: This is a repeat of the logic in _needs_site()
            if kwargs["post"] is None:
                return {"message": "That post could not be found"}, 404

            if "user" in kwargs and kwargs["user"]:
                # We have a User, check if the Post belongs to them
                kwargs["owns_post"] = (
                    kwargs["post"].user_id == kwargs["user"].id)
            else:
                # No User, no ownership
                kwargs["owns_post"] = False

            if post_owner_only:
                if not kwargs["owns_post"]:
                    return {"message": "You don't own this post"}, 401

            return function(*args, **kwargs)
        return wrapper
    return decorator


class PostsPostEndpoint(Resource):
    """
    Route used for reading, updating, deleting a single post
    """
    @_needs_post()
    def get(self, post, **kwargs):
        """Retrieves a post by it's identifier"""
        return post.to_dict(), 200

    @security(strict=True)
    @_needs_post(post_owner_only=True)
    def delete(self, post, **kwargs):
        """
        Route for deleting a post
        """
        post_slug = post.slug
        post.delete()

        return {"message": "Post '{}' deleted".format(post_slug)}, 200
