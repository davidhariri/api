from flask_restful import Resource
from bson.objectid import ObjectId

from models.article import Article
from helpers.auth import (
    security,
    fingerprint
)
from helpers.io import json_input
from helpers.paging import paginate
from helpers.cache import cached

from mongoengine.errors import (
    ValidationError,
    NotUniqueError,
    FieldDoesNotExist
)

# MARK - Constants

MSG_INVALID = "Sorry, your article could not be saved"
MSG_DUPLICATE = (
    "Sorry, that slug is already taken; "
    "Try a different article title"
)
MSG_NOT_FOUND = "Sorry, that article could not be found"
MSG_INVALID_FIELD = "Sorry, one or more of your fields do not exist"
MSG_DELETED = "Article '{title}' ({_id}) was deleted"
MSG_INVALID_ACTION = "Sorry, '{}' is not a valid action"

NON_PUBLIC_FIELDS = ["_id", "published", "shared"]
VALID_ACTIONS = {"read", "love"}

# MARK - Private helpers


def _needs_article():
    """
    Abstraction decorator for endpoints that need an article to be
    useful

    returns 404 or passes an article into the next function
    """
    def decorator(function):
        def wrapper(*args, **kwargs):
            id_or_slug = kwargs["id_or_slug"]

            query = _id_or_slug_to_query(id_or_slug)
            articles = Article.objects(**query)

            if len(articles) == 0:
                return {"message": MSG_NOT_FOUND}, 404

            kwargs["article"] = articles[0]
            del kwargs["id_or_slug"]

            return function(*args, **kwargs)
        return wrapper
    return decorator


def _save_article(article, success_code=200, response_dict=None):
    """
    Saves an article and handles validation errors etc...
    """
    try:
        article.save()
    except ValidationError as ve:
        return {
            "message": MSG_INVALID,
            "invalid": ve.to_dict()
        }, 400
    except NotUniqueError:
        return {"message": MSG_DUPLICATE}, 400
    except FieldDoesNotExist:
        return {"message": MSG_INVALID_FIELD}, 400

    if response_dict is not None:
        return response_dict, success_code

    return article.to_dict(), success_code


def _id_or_slug_to_query(id_or_slug):
    """
    Given a string that might be an objectid string or a human readable
    URL slug string, return a query dictionary that uses the correct one

    NOTE: a limitation of this function is that if a URL slug is an
    objectid, it will return a query on id instead of slug
    """
    try:
        query = {"id": ObjectId(id_or_slug)}
    except Exception:
        query = {"slug": id_or_slug}

    return query

# MARK - Endpoint Resources


class ArticlesEndpoint(Resource):
    """
    Routes defined for manipluating Article objects
    """
    @security(True)
    @json_input(Article._fields)
    def post(self, authorized, fields):
        """
        Endpoint for creating new Articles
        """
        article = Article(**fields)

        if article.title is None:
            return {
                "invalid": {
                    "title": "Field is required"
                },
                "message": MSG_INVALID
            }, 400

        return _save_article(article, 201)

    @security()
    @paginate()
    @cached(namespace="articles", expiry=60)
    def get(self, authorized, limit, skip, order):
        """
        Endpoint for listing articles
        """
        query = {}
        ignore_fields = []

        if not authorized:
            query = {"published": True}
            ignore_fields = NON_PUBLIC_FIELDS

        articles = Article.objects(**query).order_by(order).skip(
            skip).limit(limit)

        return {
            "articles": list(
                map(lambda a: a.to_dict(ignore_fields), articles)
            )
        }


class ArticleEndpoint(Resource):
    """
    Route used for reading, updating, deleting a single article
    """
    @security()
    @_needs_article()
    @cached(namespace="articles", expiry=60)
    def get(self, article, authorized):
        """Retrieves an article by it's identifier"""
        if authorized:
            ignore_fields = []
        else:
            if not article.published and not article.shared:
                return {"message": MSG_NOT_FOUND}, 404

            ignore_fields = NON_PUBLIC_FIELDS

        return article.to_dict(ignore_fields), 200

    @security(True)
    @json_input(Article._fields)
    @_needs_article()
    def patch(self, article, fields, **kwargs):
        """
        Route for modifying a single article's fields. This endpoint is
        protected
        """
        article.update_fields(fields)

        return _save_article(article)

    @security(True)
    @_needs_article()
    def delete(self, article, authorized, **kwargs):
        """
        Route for deleting an article
        """
        article.delete()

        return {
            "message": MSG_DELETED.format(**article.to_dict())
        }, 200


class ArticleActionsEndpoint(Resource):
    """
    Route to perform certain actions on an Article like read, like etc.
    """
    @fingerprint(True)
    @_needs_article()
    def put(self, article, action, **kwargs):
        if action in VALID_ACTIONS:
            if action == "love":
                article.increment_love_count()
            elif action == "read":
                article.increment_read_count()
        else:
            return {
                "message": MSG_INVALID_ACTION.format(action)
            }, 400

        return _save_article(article, response_dict={"message": "OK"})
