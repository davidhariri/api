from flask import request


def json_input(allowed_fields=[], can_be_empty=False):
    """
    Protects patch and post endpoints from having to validate that
    incoming field data is JSON serialized, valid and non-empty
    """
    def decorator(function):
        def wrapper(*args, **kwargs):
            fields = request.get_json()

            if fields is None:
                return {
                    "message": (
                        "Sorry, your request body data should be"
                        " JSON serialized"
                    )
                }, 400

            if isinstance(allowed_fields, dict):
                allowed_keys = set(allowed_fields.keys())

            input_keys = set(fields.keys())

            for k in input_keys:
                if k not in allowed_keys:
                    del fields[k]

            if len(fields.keys()) == 0 and not can_be_empty:
                return {
                    "message": "Sorry, you need to pass in some fields"
                }, 400

            kwargs["fields"] = fields

            return function(*args, **kwargs)
        return wrapper
    return decorator
