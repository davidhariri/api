from flask_restful import Resource
from mongoengine.queryset.visitor import Q
from models.article import Article
from bson.objectid import ObjectId

MSG_NOT_FOUND = "Sorry, that article could not be found"


class ArticleEndpoint(Resource):
    """
    Route used for reading, updating, deleting a single article
    """
    def get(self, id_or_slug):
        """Retrieves an article by it's identifier"""
        # TODO: Use authentication to block access to unpublished
        # articles

        try:
            id_or_slug = ObjectId(id_or_slug)
            query = {"id": id_or_slug}
        except Exception:
            query = {"slug": id_or_slug}
            pass

        articles = Article.objects(**query)

        if len(articles) == 0:
            return {"message": MSG_NOT_FOUND}, 404

        return articles[0].to_dict(), 200
