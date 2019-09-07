from flask_restful import Resource
from flask import request
from sentry_sdk import capture_exception
from helpers.db import db
from models.media import Media, InvalidMediaTypeException
from helpers.s3 import upload
from helpers.auth import security
import os

CDN_URI = "https://static.little.site/media/{}"


class MediaEndpoint(Resource):
    """
    Routes defined for uploading images to the CDN
    """
    @security(True)
    def post(self, user, **kwargs):
        """Base endpoint"""
        file = request.files["file"]

        try:
            media = Media(file=file)
            media.user_id = user.id
        except InvalidMediaTypeException as e:
            return {
                "message": str(e)
            }, 400

        optimized_file_names = media.optimize()

        for file_name in optimized_file_names:
            upload(file_name)
            os.remove(file_name)

        media.url = CDN_URI.format(optimized_file_names[0])
        media.url_optimized = CDN_URI.format(optimized_file_names[1])

        if len(optimized_file_names) is 3:
            media.url_poster = CDN_URI.format(optimized_file_names[2])

        media.showcase = request.args.get("showcase") is not None

        try:
            media.save()
        except Exception as e:
            capture_exception(e)
            return {
                "message": "An unexpected error occoured while writing to the database"
            }, 400

        return media.to_dict(), 201
