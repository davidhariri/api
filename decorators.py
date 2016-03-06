from config import settings
from functools import wraps
from flask import request

# Read in the admin of the API from the settings file
auth_user = settings["authentication"]

# TODO: Default to returning 401 if not passed?

def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Assume we're not authenticated:
        kwargs["authenticated"] = None

        if request.authorization != None:
            # An authentication header was passed. Let's verify it's the admin:
            if request.authorization.username == auth_user["email"] and request.authorization.password == auth_user["pass"]:
                # Authorized!
                kwargs["authenticated"] = True
            else:
                kwargs["authenticated"] = False

        # Pass everything back to the next function
        return f(*args, **kwargs)
    return wrapper
