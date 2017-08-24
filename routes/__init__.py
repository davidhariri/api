from routes.notes import (
    NotesEndpoint,
    NoteEndpoint,
    NoteActionsEndpoint
)
from routes.root import RootEndpoint
from routes.auth import AuthEndpoint
from routes.images import ImagesEndpoint

route_dict = {
    "/": RootEndpoint,
    "/auth/": AuthEndpoint,
    "/notes/": NotesEndpoint,
    "/notes/<string:id_or_slug>/": NoteEndpoint,
    "/notes/<string:id_or_slug>/<string:action>/": NoteActionsEndpoint,
    "/images/": ImagesEndpoint
}
