from flask_restful import Resource

from models.post import Post
from models.site import Site
from helpers.auth import (
    security
)
from helpers.io import json_input
from helpers.paging import paginate
from sqlalchemy import desc


ALLOWED_POST_FIELDS = [
    "comment",
    "public",
    "location_lat",
    "location_lon",
    "location_name",
    "review",
    "link_name",
    "link_uri",
    "media",
    "topics"
]

ALLOWED_SITE_FIELDS = [
    "handle"
]


def _needs_site(site_owner_only=False):
    """
    Abstraction decorator for endpoints that need a site to be
    useful
    """
    def decorator(function):
        def wrapper(*args, **kwargs):
            kwargs["site"] = Site.query.filter(
                Site.handle == kwargs["site_handle"]).first()
            del kwargs["site_handle"]

            # NOTE: This is a repeat of the logic in _needs_post()
            # Could we find a Site for that handle?
            if kwargs["site"] is None:
                return {"message": "Could not find that site"}, 404

            if "user" in kwargs and kwargs["user"]:
                # We have a User, check if the Site belongs to them
                kwargs["owns_site"] = (
                    kwargs["site"].user_id == kwargs["user"].id)
            else:
                # No User, no ownership
                kwargs["owns_site"] = False

            if site_owner_only:
                if not kwargs["owns_site"]:
                    return {"message": "You don't own this site"}, 401

            return function(*args, **kwargs)
        return wrapper
    return decorator


class SitesEndpoint(Resource):
    """
    /sites/
    https://www.notion.so/littlesite/Sites-86d257e0f5da49c49404a974af474acc#8f073b0558f046ce97be7349ec5609cb
    """
    @security(strict=True)
    @json_input(ALLOWED_SITE_FIELDS)
    def post(self, user, fields, **kwargs):
        """
        Create a new Site with a handle field
        """
        h = fields["handle"]

        if not isinstance(h, str) or len(h) == 0:
            return {
                "message": "handle must be a non-empty string"
            }, 400

        new_site = Site(**fields)
        new_site.user_id = user.id
        new_site.set_first_handle(h)

        return new_site.to_dict(), 201


class SitesSiteEndpoint(Resource):
    """
    /sites/<site_handle>/
    https://www.notion.so/littlesite/Sites-86d257e0f5da49c49404a974af474acc#ce93d0b9347646928e14ae9ed0503cce
    """
    @security(strict=True)
    @_needs_site(site_owner_only=True)
    def delete(self, site, **kwargs):
        """
        Delete a Site and all associated Posts
        """
        site_handle = site.handle
        site.delete()

        return {"message": "Site '{}' deleted".format(site_handle)}, 200


class SitesSitePostsEndpoint(Resource):
    """
    /sites/<site_handle>/posts/
    https://www.notion.so/littlesite/Sites-86d257e0f5da49c49404a974af474acc#cf08deadb11444d59d5bd26cb8e911fb
    """
    @security(strict=True)
    @_needs_site(site_owner_only=True)
    @json_input(ALLOWED_POST_FIELDS)
    def post(self, user, site, fields, **kwargs):
        """
        Add a Post to a Site
        """
        post = Post(**fields)
        post.user_id = user.id
        post.site_id = site.id
        post.save()

        return post.to_dict(), 201

    @security()
    @_needs_site()
    @paginate()
    def get(self, site, owns_site, skip, limit, **kwargs):
        """
        List all public Posts for a Site
        If authenticated and it's your site, list all private Posts too
        """
        query = {"site_id": site.id}

        if not owns_site:
            query = {"public": True}

        posts = Post.query.filter_by(**query).order_by(
            desc(Post.date_created)).offset(skip).limit(limit)

        return {
            "posts": list(
                map(lambda p: p.to_dict(), posts)
            )
        }, 200
