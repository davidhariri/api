from routes.articles import (
    ArticlesEndpoint,
    ArticleEndpoint,
    # ArticleActionsEndpoint
)
from routes.root import RootEndpoint

route_dict = {
    "/articles/": ArticlesEndpoint,
    "/articles/<string:id_or_slug>/": ArticleEndpoint,
    # "/articles/<string:id_or_slug>/<string:action>/": ArticleActionsEndpoint,
    "/": RootEndpoint
}
