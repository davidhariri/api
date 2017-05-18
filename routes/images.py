from flask_restful import Resource
from flask import request
import tinys3
import os
import uuid

_ALLOWED_TYPES = set(["png", "jpg", "jpeg", "gif", "svg"])
_MSG_BAD_FORMAT = "Sorry, '{}' is not a supported format"


class ImagesEndpoint(Resource):
    """
    Routes defined for manipluating images (for blog posts etc..)
    """
    def post(self):
        """Base endpoint"""
        bucket = tinys3.Connection(
            os.getenv("S3_ACCESS_KEY"),
            os.getenv("S3_SECRET_KEY"),
            tls=True)

        file = request.files["file"]
        file_extension = file.filename.split(".")[-1]
        file_name = "{}.{}".format(uuid.uuid4(), file_extension)

        if file_extension in _ALLOWED_TYPES:
            bucket.upload(
                ("images/" + file_name),
                file,
                os.getenv("S3_BUCKET_NAME")
            )
        else:
            return {
                "message": _MSG_BAD_FORMAT.format(file_extension)
            }, 400

        return {"message": "OK"}, 200
