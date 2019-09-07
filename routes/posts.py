from helpers.db import db
from flask_restful import Resource
from flask import request
from helpers.cache import invalidate

from models.post import Post
from helpers.auth import (
    security,
    fingerprint
)
from helpers.io import json_input
from helpers.paging import paginate
from helpers.twitter import post_post_as_tweet
from helpers.cache import cached
from sqlalchemy import desc


# MARK - Constants

MSG_INVALID = "Sorry, your post could not be saved"
MSG_DUPLICATE = (
    "Sorry, that slug is already taken; "
    "Try a different post title"
)
MSG_NOT_FOUND = "Sorry, that post could not be found"
MSG_UNEXPECTED = "Sorry, an unexpected error has occoured"
MSG_INVALID_FIELD = "Sorry, one or more of your fields do not exist"
MSG_DELETED = "Post '{slug}' was deleted"
MSG_INVALID_ACTION = "Sorry, '{}' is not a valid action"

VALID_ACTIONS = {"love"}

# MARK - Private helpers


def _needs_post():
    """
    Abstraction decorator for endpoints that need a post to be
    useful

    returns 404 or passes an post into the next function
    """
    def decorator(function):
        def wrapper(*args, **kwargs):
            kwargs["post"] = Post.query.filter(Post.slug == kwargs["slug_str"]).first()

            del kwargs["slug_str"]

            if kwargs["post"] is None:
                return {"message": MSG_NOT_FOUND}, 404

            return function(*args, **kwargs)
        return wrapper
    return decorator


def _save_post(post, success_code=200):
    """
    Saves a post and handles validation errors etc...
    """
    try:
        db.session.add(post)
        db.session.commit()
    except Exception as e:
        print(e)
        return {
            "message": MSG_INVALID
        }, 400
    # except NotUniqueError:
    #     return {"message": MSG_DUPLICATE}, 400
    # except FieldDoesNotExist:
    #     return {"message": MSG_INVALID_FIELD}, 400

    # Invalidate cached posts
    invalidate("post")

    return post.to_dict(), success_code


def _has_topics():
    def decorator(function):
        def wrapper(*args, **kwargs):
            kwargs["topics"] = request.args.getlist("topic")
            return function(*args, **kwargs)
        return wrapper
    return decorator

# MARK - Endpoint Resources


ALLOWED_FIELDS = [
    "comment",
    "public",
    "location_lat",
    "location_lon",
    "location_name",
    "review",
    "link_name",
    "link_uri",
    "media",
    "topics",
    "site_id"
]


class PostEndpoint(Resource):
    """
    Route used for reading, updating, deleting a single post
    """
    @security()
    @_needs_post()
    def get(self, post, authorized, **kwargs):
        """Retrieves a post by it's identifier"""
        return post.to_dict(), 200

    @security(True)
    @_needs_post()
    def delete(self, post, authorized, **kwargs):
        """
        Route for deleting a post
        """
        # TODO: Check to ensure the user owns this post
        db.session.delete(post)
        db.session.commit()

        return {
            "message": MSG_DELETED.format(**post.to_dict())
        }, 200

