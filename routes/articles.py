from flask_restful import Resource
from flask import request
from bson.objectid import ObjectId
from mongoengine.queryset.visitor import Q

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
MSG_NOT_FOUND = "Sorry, that article could not be found"


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


class ArticleEndpoint(Resource):
    """
    Route used for reading, updating, deleting a single article
    """
    @security(False)
    def get(self, id_or_slug, authorized):
        """Retrieves an article by it's identifier"""

        try:
            id_or_slug = ObjectId(id_or_slug)
            query = {"id": id_or_slug}
        except Exception:
            query = {"slug": id_or_slug}
            pass

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

    def patch(self, id_or_slug, authorized):
        """
        Route for modifying a single article. This endpoint is
        protected
        """
        pass
