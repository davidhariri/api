from flask_restful import Resource
from bson.objectid import ObjectId
from mongoengine.queryset.visitor import Q

from models.article import Article
from helpers.auth import security
from helpers.io import json_input

from mongoengine.errors import (
    ValidationError,
    NotUniqueError,
    FieldDoesNotExist
)

MSG_INVALID = "Sorry, your article could not be saved"
MSG_DUPLICATE = (
    "Sorry, that slug is already taken; "
    "Try a different article title"
)
MSG_NOT_FOUND = "Sorry, that article could not be found"
MSG_INVALID_FIELD = "Sorry, one or more of your fields do not exist"

# MARK - Private helpers


def _save_article(article, success_code=200):
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

    print(article.title)

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
    def get(self, authorized):
        """
        Endpoint for listing articles
        """
        if authorized:
            articles = Article.objects()
            ignore_fields = []
        else:
            articles = Article.objects(published=True)
            ignore_fields = ["_id", "published", "shared", "share_handle"]

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
    def get(self, id_or_slug, authorized):
        """Retrieves an article by it's identifier"""
        query = _id_or_slug_to_query(id_or_slug)

        if authorized:
            articles = Article.objects(**query)
            ignore_fields = []
        else:
            articles = Article.objects.filter(
                Q(**query) & (Q(shared=True) | Q(published=True))
            )
            ignore_fields = ["_id", "published", "shared", "share_handle"]

        if len(articles) == 0:
            return {"message": MSG_NOT_FOUND}, 404

        return articles[0].to_dict(ignore_fields), 200

    @security(True)
    @json_input(Article._fields)
    def patch(self, id_or_slug, authorized, fields):
        """
        Route for modifying a single article's fields. This endpoint is
        protected
        """
        query = _id_or_slug_to_query(id_or_slug)
        articles = Article.objects(**query)

        if len(articles) == 0:
            return {"message": MSG_NOT_FOUND}, 404

        article = articles[0]
        article.modify(**fields)

        return _save_article(article)
