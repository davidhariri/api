from flask import request
import uuid
import hashlib

from models.token import AuthToken


def fingerprint(strict=False):
    """
    Endpoint fingerprinting bases on request headers. Allows for public
    actions to be performed without authentication like reading, liking
    etc...

    if strict, we should throw a 429 Too many requests if the
    fingerprint is in Redis
    """
    def decorator(function):
        def wrapper(*args, **kwargs):
            k = (
                request.headers.get("User-Agent", "") +
                request.remote_addr
            )
            k = k.encode("utf-8")

            key_digest = namespace + hashlib.md5(k).hexdigest()

            kwargs["fingerprint"] = key_digest

            return function(*args, **kwargs)
        return wrapper
    return decorator


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
