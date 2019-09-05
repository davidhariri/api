from helpers.db import db
from flask_restful import Resource
from flask import request

from models.site import Site
from helpers.auth import (
    security
)
from helpers.paging import paginate
from helpers.cache import cached
from sqlalchemy import desc

MSG_ACCESS_DENIED = "Sorry, you can only list your own sites at this time"


class UsersSitesEndpoint(Resource):
    """
    Routes defined for manipluating Post objects
    """
    @security(True)
    @paginate()
    @cached(namespace="users", expiry=60)
    def get(self, user, user_id, limit, skip, **kwargs):
        """
        Endpoint for listing a User's Sites

        ://api.little.site/users/1/sites/
        """

        # Check to ensure the user is asking for their own sites
        if user.id is not int(user_id):
            return {
                "message": MSG_ACCESS_DENIED
            }, 401

        sites = Site.query.filter_by(user_id=user_id).order_by(desc(Site.date_created)).offset(skip).limit(limit)

        return {
            "sites": list(
                map(lambda s: s.to_dict(), sites)
            )
        }, 200
