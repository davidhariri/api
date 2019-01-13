import tinys3
import os
import io


def upload(file_name):
    bucket = tinys3.Connection(
        os.getenv("S3_ACCESS_KEY"),
        os.getenv("S3_SECRET_KEY"),
        tls=True)

    file = open(file_name, 'rb')

    bucket.upload(
        ("media/" + file_name),
        file,
        os.getenv("S3_BUCKET_NAME")
    )
