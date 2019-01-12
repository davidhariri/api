from flask_restful import Resource
from flask import request
from helpers.db import db
from models.media import Media, InvalidMediaTypeException
from helpers.s3 import upload
from helpers.auth import security
import os

CDN_URI = "https://static.dhariri.com/images/{}"


class ImagesEndpoint(Resource):
    """
    Routes defined for manipluating images (for blog posts etc..)
    """
    @security(True)
    def post(self, **kwargs):
        """Base endpoint"""
        file = request.files["file"]

        try:
            media = Media(file=file)
        except InvalidMediaTypeException as e:
            return {
                "message": str(e)
            }, 400

        optimized_file_names = media.optimize()

        for file_name in optimized_file_names:
            upload(file_name)
            os.remove(file_name)

        media.url_raw = CDN_URI.format(optimized_file_names[0])
        media.url_optimized = CDN_URI.format(optimized_file_names[1])

        # TODO: Pull showcase bool from url arguments
        # TODO: try/except
        db.session.add(media)
        db.session.commit()

        return media.to_dict(), 200
