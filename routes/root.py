from flask_restful import Resource


class RootEndpoint(Resource):
    def get(self):
        """Base endpoint"""
        return {"message": "What hath God wrought?"}, 200
