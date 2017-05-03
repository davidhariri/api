from flask import request
import uuid

from models.token import AuthToken


def security(strict=False):
    """
    Main endpoint security decorator.
    strict=True means a token is needed for this endpoint
    strict=False means this endpoint changes it's response with a token
    """
    def decorator(function):
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization")

            if strict and token is None:
                return {
                    "message": "Missing Authorization Token"
                }, 401

            try:
                token = uuid.UUID(token)
            except Exception:
                token = None

            if strict and token is None:
                return {
                    "message": "Malformed Authorization Token"
                }, 400

            if not strict and token is None:
                kwargs["authorized"] = False

            if token is not None:
                matched_tokens = AuthToken.objects(token=token)

                if len(matched_tokens) == 0 and strict:
                    return {
                        "message": "Incorrect Authorization Token"
                    }, 403

                kwargs["authorized"] = (len(matched_tokens) > 0)
            else:
                kwargs["authorized"] = False

            return function(*args, **kwargs)
        return wrapper
    return decorator
