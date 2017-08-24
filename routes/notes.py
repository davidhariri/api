from flask_restful import Resource
from bson.objectid import ObjectId
from mongoengine.queryset.visitor import Q

from mongoengine.errors import (
    ValidationError,
    NotUniqueError,
    FieldDoesNotExist
)

from models.note import Note
from helpers.auth import (
    security,
    fingerprint
)
from helpers.io import json_input
from helpers.paging import paginate
from helpers.cache import cached

# MARK - Constants

MSG_INVALID = "Sorry, your note could not be saved"
MSG_DUPLICATE = (
    "Sorry, that slug is already taken; "
    "Try a different note title"
)
MSG_NOT_FOUND = "Sorry, that note could not be found"
MSG_INVALID_FIELD = "Sorry, one or more of your fields do not exist"
MSG_DELETED = "Note '{slug}' was deleted"
MSG_INVALID_ACTION = "Sorry, '{}' is not a valid action"

VALID_ACTIONS = {"read", "love"}

# MARK - Private helpers


def _id_or_slug_to_query(id_or_slug):
    """
    Given a string that might be an objectid string or a human readable
    URL slug string, return a query dictionary that uses the correct one

    NOTE: a limitation of this function is that if a URL slug is an
    objectid, it will return a query on id instead of slug
    """
    try:
        query = {"id": ObjectId(id_or_slug)}
    except Exception:
        query = {"slug": id_or_slug}

    return query


def _needs_note():
    """
    Abstraction decorator for endpoints that need a note to be
    useful

    returns 404 or passes an note into the next function
    """
    def decorator(function):
        def wrapper(*args, **kwargs):
            id_or_slug = kwargs["id_or_slug"]

            query = _id_or_slug_to_query(id_or_slug)
            notes = Note.objects(**query)

            if len(notes) == 0:
                return {"message": MSG_NOT_FOUND}, 404

            kwargs["note"] = notes[0]
            del kwargs["id_or_slug"]

            return function(*args, **kwargs)
        return wrapper
    return decorator


def _save_note(note, success_code=200, response_dict=None):
    """
    Saves an note and handles validation errors etc...
    """
    try:
        note.save()
    except ValidationError as ve:
        return {
            "message": MSG_INVALID,
            "invalid": ve.to_dict()
        }, 400
    except NotUniqueError:
        return {"message": MSG_DUPLICATE}, 400
    except FieldDoesNotExist:
        return {"message": MSG_INVALID_FIELD}, 400

    if response_dict is not None:
        return response_dict, success_code

    return note.to_dict(), success_code

# MARK - Endpoint Resources


class NotesEndpoint(Resource):
    """
    Routes defined for manipluating Note objects
    """
    @security(True)
    @json_input(Note._fields)
    def post(self, authorized, fields):
        """
        Endpoint for creating new Notes
        """
        note = Note(**fields)

        return _save_note(note, 201)

    @security()
    @paginate()
    @cached(namespace="note", expiry=60)
    def get(self, authorized, limit, skip, order):
        """
        Endpoint for listing notes
        """
        query = {}

        if not authorized:
            query = {"public": True}

        notes = Note.objects(**query).order_by(order).skip(
            skip).limit(limit)

        return {
            "notes": list(
                map(lambda n: n.to_dict(), notes)
            )
        }


class NoteEndpoint(Resource):
    """
    Route used for reading, updating, deleting a single note
    """
    @security()
    @_needs_note()
    @cached(namespace="note", expiry=60)
    def get(self, note, authorized):
        """Retrieves a note by it's identifier"""
        return note.to_dict(), 200

    @security(True)
    @json_input(Note._fields)
    @_needs_note()
    def patch(self, note, fields, **kwargs):
        """
        Route for modifying a single note's fields. This endpoint is
        protected
        """
        note.update_fields(fields)

        return _save_note(note)

    @security(True)
    @_needs_note()
    def delete(self, note, authorized, **kwargs):
        """
        Route for deleting an note
        """
        note.delete()

        return {
            "message": MSG_DELETED.format(**note.to_dict())
        }, 200


class NoteActionsEndpoint(Resource):
    """
    Route to perform certain actions on an Note like read, like etc.
    """
    @fingerprint(True)
    @_needs_note()
    def put(self, note, action, **kwargs):
        if action in VALID_ACTIONS:
            if action == "love":
                note.increment_love_count()
        else:
            return {
                "message": MSG_INVALID_ACTION.format(action)
            }, 400

        return _save_note(note, response_dict={"message": "OK"})
