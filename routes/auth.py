from helpers.auth import security
from flask_restful import Resource


class AuthEndpoint(Resource):
    """
    Routes defined for checking authentication of clients
    """
    @security(True)
    def get(self, **kwargs):
        """Base auth test endpoint"""
        # If you get this far in endpoints that have @security(True)
        # Then a Token and a User exist in the kwargs
        return {
            "user": kwargs["user"].to_dict()
        }, 200
