from routes.articles import Articles
from routes.root import Root

route_dict = {
    "/articles/": Articles,
    "/": Root
}
