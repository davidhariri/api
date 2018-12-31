from flask import request


def paginate(d_limit=10, d_page=1):
    """
    Decorator for parsing paging parameters with some useful defaults
    """
    def decorator(function):
        def wrapper(*args, **kwargs):
            l = int(request.args.get("size", d_limit))
            s = (int(request.args.get("page", d_page)) - 1) * l

            kwargs.update({
                "limit": l,
                "skip": s
            })

            return function(*args, **kwargs)
        return wrapper
    return decorator
