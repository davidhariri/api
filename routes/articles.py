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


class Articles(Resource):
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

        if article.slug is None:
            article.generate_slug()

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

    @security(False)
    def get(self, authorized):
        """
        Endpoint for listing articles
        """
        articles = Article.objects(published=True)
        public_ignore = ["_id", "published", "shared", "share_handle"]

        return {
            "articles": list(
                map(lambda a: a.to_dict(public_ignore), articles)
            )
        }
