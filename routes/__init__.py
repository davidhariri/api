from routes.articles import ArticlesEndpoint
from routes.article import ArticleEndpoint
from routes.root import RootEndpoint

route_dict = {
    "/articles/": ArticlesEndpoint,
    "/articles/<string:id_or_slug>/": ArticleEndpoint,
    "/": RootEndpoint
}
