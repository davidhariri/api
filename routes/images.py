from flask_restful import Resource
from flask import request
import tinys3
import os
import uuid
from helpers.auth import security

_ALLOWED_TYPES = set([
    "image/png",
    "image/jpg",
    "image/jpeg",
    "image/svg",
    "image/svg+xml",
    "image/gif"
])
_MSG_BAD_FORMAT = "Sorry, '{}' is not a supported format"


class ImagesEndpoint(Resource):
    """
    Routes defined for manipluating images (for blog posts etc..)
    """
    @security(True)
    def post(self, **kwargs):
        """Base endpoint"""
        bucket = tinys3.Connection(
            os.getenv("S3_ACCESS_KEY"),
            os.getenv("S3_SECRET_KEY"),
            tls=True)

        file = request.files["file"]
        file_extension = file.filename.split(".")[-1]
        file_name = "{}.{}".format(uuid.uuid4(), file_extension)

        if file.content_type not in _ALLOWED_TYPES:
            return {
                "message": _MSG_BAD_FORMAT.format(file_extension)
            }, 400

        bucket.upload(
            ("images/" + file_name),
            file,
            os.getenv("S3_BUCKET_NAME")
        )

        return {
            "url": "https://static.dhariri.com/images/{}".format(
                file_name
            )
        }, 200
