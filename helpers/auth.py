from flask import request
import uuid
import hashlib
from models.token import AuthToken
from models.user import User
from helpers.cache import cache

# MARK - Constants

MSG_TOO_MANY = "Sorry, you've performed this request too many times"


def fingerprint(strict=False, expiry=(60 * 60), namespace="ls-fingerprint"):
    """
    Endpoint fingerprinting bases on request headers. Allows for public
    actions to be performed without authentication like reading, liking
    etc...

    if strict, we should throw a 429 Too many requests if the
    fingerprint is in Redis
    """
    def decorator(function):
        def wrapper(*args, **kwargs):
            r_addr = request.remote_addr
            # Use X-Forwareded-For first because of Heroku's balancers
            client_ip = request.headers.get("X-Forwarded-For", r_addr)

            to_digest = (
                request.headers.get("User-Agent", "") +
                client_ip + request.path
            )

            to_digest = to_digest.encode("utf-8")

            digest = namespace + hashlib.md5(to_digest).hexdigest()

            if strict:
                if cache.exists(digest):
                    return {
                        "message": MSG_TOO_MANY
                    }, 429
                else:
                    cache.setex(name=digest, value=1, time=expiry)

            kwargs["fingerprint"] = digest

            return function(*args, **kwargs)
        return wrapper
    return decorator


def _find_user(user_id):
    """
    Simple finder function for getting User objects and caching results
    """
    # TODO: What happens if the user is deleted, but the token is still used?
    return User.query.get(user_id)


def _find_token(token_str):
    """
    Simple finder function which allows for more specific caching
    """
    return AuthToken.query.filter_by(token=token_str).first()


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
                matched_token = _find_token(token_str=token)

                if matched_token is None and strict:
                    return {
                        "message": "Incorrect Authorization Token"
                    }, 403

                if matched_token is not None:
                    # Find the User that matches the token
                    kwargs["authorized"] = True
                    kwargs["token"] = matched_token
                    kwargs["user"] = _find_user(matched_token.user_id)

                else:
                    # No matched token, request is not authorized, but the
                    # caller may still do things
                    kwargs["authorized"] = False

            else:
                kwargs["authorized"] = False

            return function(*args, **kwargs)
        return wrapper
    return decorator
