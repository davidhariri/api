from flask_restful import Resource


class RootEndpoint(Resource):
    def get(self):
        """Base atlas endpoint"""
        return {
            "documentation": "https://github.com/davidhariri/api/blob/master/README.md",
            "atlas": [
                {
                    "decription": "See all the public notes",
                    "path": "/notes/"
                },
                {
                    "description": "See a single note (public or private)",
                    "path": "/notes/<note_id_or_slug>/"
                }
            ]
        }, 200
