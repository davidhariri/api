from flask_restful import Resource
from mongoengine.queryset.visitor import Q
from models.article import Article
from bson.objectid import ObjectId
from helpers.auth import security

MSG_NOT_FOUND = "Sorry, that article could not be found"


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
        else:
            articles = Article.objects.filter(
                Q(**query) & (Q(shared=True) | Q(published=True))
            )

        if len(articles) == 0:
            return {"message": MSG_NOT_FOUND}, 404

        if authorized:
            ignore_fields = []
        else:
            ignore_fields = ["_id", "published", "shared", "share_handle"]

        return articles[0].to_dict(ignore_fields), 200
