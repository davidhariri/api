from flask import request
import uuid
import hashlib
from redis import StrictRedis
import os
from models.token import AuthToken

redis = StrictRedis.from_url(
    os.getenv("REDIS_URI", "redis://localhost:6379/0"))

# MARK - Constants

MSG_TOO_MANY = "Sorry, you've performed this request too many times"


def fingerprint(strict=False, expiry=(60 * 60), namespace="dhariri"):
    """
    Endpoint fingerprinting bases on request headers. Allows for public
    actions to be performed without authentication like reading, liking
    etc...

    if strict, we should throw a 429 Too many requests if the
    fingerprint is in Redis
    """
    def decorator(function):
        def wrapper(*args, **kwargs):
            to_digest = (
                request.headers.get("User-Agent", "") +
                request.remote_addr +
                request.path
            )
            to_digest = to_digest.encode("utf-8")

            digest = namespace + hashlib.md5(to_digest).hexdigest()

            if strict:
                if redis.exists(digest):
                    return {
                        "message": MSG_TOO_MANY
                    }, 429
                else:
                    redis.setex(digest, expiry, 1)

            kwargs["fingerprint"] = digest

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
