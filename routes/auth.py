from helpers.auth import security
from flask_restful import Resource


class AuthEndpoint(Resource):
    """
    Routes defined for checking authentication of clients
    """
    @security(True)
    def get(self, **kwargs):
        """Base endpoint"""
        print(kwargs["user"])
        return {"message": "Hello World"}, 200
