from flask_restful import Resource


class RootEndpoint(Resource):
    """
    Routes defined for manipluating Article objects
    """
    def get(self):
        """Base endpoint"""
        return {"message": "What hath God wrought?"}, 200
