from routes.sites import (
    SitesEndpoint,
    SitesSiteEndpoint,
    SitesSitePostsEndpoint
)
from routes.posts import PostsPostEndpoint
from routes.auth import AuthEndpoint
from routes.media import MediaEndpoint
from routes.users import UsersSitesEndpoint

route_dict = {
    "/auth/": AuthEndpoint,
    "/users/<int:user_id>/sites/": UsersSitesEndpoint,
    "/sites/": SitesEndpoint,
    "/sites/<string:site_handle>/": SitesSiteEndpoint,
    "/sites/<string:site_handle>/posts/": SitesSitePostsEndpoint,
    "/posts/<string:post_slug>/": PostsPostEndpoint,
    "/media/": MediaEndpoint
}
