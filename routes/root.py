from flask_restful import Resource
from helpers.auth import security

class RootEndpoint(Resource):
    """
    Routes defined for manipluating Article objects
    """
    @security()
    def get(self, authorized):
        """Base endpoint"""
        if authorized:
            return {"message": "What hath God wrought?"}, 200
        else:
            return {"message": "Hello World"}, 200
