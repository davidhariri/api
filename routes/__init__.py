from routes.articles import (
    ArticlesEndpoint,
    ArticleEndpoint,
    ArticleActionsEndpoint
)
from routes.root import RootEndpoint
from routes.images import ImagesEndpoint

route_dict = {
    "/": RootEndpoint,
    "/articles/": ArticlesEndpoint,
    "/articles/<string:id_or_slug>/": ArticleEndpoint,
    "/articles/<string:id_or_slug>/<string:action>/": ArticleActionsEndpoint,
    "/images/": ImagesEndpoint
}
