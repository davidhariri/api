from routes.posts import (
    PostsEndpoint,
    PostEndpoint,
    PostActionsEndpoint
)
from routes.root import RootEndpoint
from routes.auth import AuthEndpoint
from routes.media import MediaEndpoint

# Exported dictionary which matches paths to routes for cleaner code organization

route_dict = {
    "/": RootEndpoint,
    "/auth/": AuthEndpoint,
    "/posts/": PostsEndpoint,
    "/posts/<string:slug_str>/": PostEndpoint,
    "/posts/<string:slug_str>/<string:action>/": PostActionsEndpoint,
    "/media/": MediaEndpoint
}
