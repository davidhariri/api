from flask_restful import Resource
from flask import request

from models.article import Article
from helpers.auth import security

from mongoengine.errors import (
    ValidationError,
    NotUniqueError
)

MSG_INVALID = "Sorry, your article could not be saved"
MSG_DUPLICATE = (
    "Sorry, that slug is already taken; "
    "Try a different article title"
)


class ArticlesEndpoint(Resource):
    """
    Routes defined for manipluating Article objects
    """
    @security(True)
    def post(self, authorized):
        """
        Endpoint for creating new Articles
        """
        fields = request.get_json() or {}
        article = Article(**fields)

        if article.title is None:
            return {
                "invalid": {
                    "title": "Field is required"
                },
                "message": MSG_INVALID
            }, 400

        try:
            article.save()
        except ValidationError as ve:
            return {
                "message": MSG_INVALID,
                "invalid": ve.to_dict()
            }, 400
        except NotUniqueError:
            return {"message": MSG_DUPLICATE}, 400

        return article.to_dict(), 201

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
