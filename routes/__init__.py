from routes.posts import (
    PostsEndpoint,
    PostEndpoint,
    PostActionsEndpoint
)
from routes.root import RootEndpoint
from routes.auth import AuthEndpoint
from routes.media import MediaEndpoint
from routes.users import UsersSitesEndpoint

route_dict = {
    "/": RootEndpoint,
    "/auth/": AuthEndpoint,
    "/users/<int:user_id>/sites/": UsersSitesEndpoint,
    "/posts/": PostsEndpoint,
    "/posts/<string:slug_str>/": PostEndpoint,
    "/posts/<string:slug_str>/<string:action>/": PostActionsEndpoint,
    "/media/": MediaEndpoint
}
