from flask_restful import Resource

# TODO: Make this endpoint respond with current logged in user info
class RootEndpoint(Resource):
    def get(self):
        """Base atlas endpoint"""
        return {
            "documentation": "https://github.com/davidhariri/api/blob/master/README.md",
            "atlas": [
                {
                    "decription": "See all the public posts",
                    "path": "/posts/"
                },
                {
                    "description": "See a single post (public or private)",
                    "path": "/posts/<post_slug_str>/"
                }
            ]
        }, 200
