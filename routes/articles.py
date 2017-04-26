from flask_restful import Resource
from flask import request

from models.article import Article

from mongoengine.errors import (
    ValidationError)

MSG_INVALID = "Sorry, your article could not be saved"
EMPTY_BODY = "You need some fields there "


class Articles(Resource):
    """
    Routes defined for manipluating Article objects
    """
    def post(self):
        """
        Endpoint for creating new Articles
        """
        fields = request.get_json() or {}
        a = Article(**fields)
        a.generate_slug()

        try:
            a.save()
        except ValidationError as ve:
            return {
                "message": MSG_INVALID,
                "invalid": ve.to_dict()
            }, 400

        return a.to_dict(), 201
