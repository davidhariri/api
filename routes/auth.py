from helpers.auth import security
from helpers.db import db
from helpers.io import json_input
from flask_restful import Resource
from google.oauth2 import id_token
from google.auth.transport import requests
from sqlalchemy.exc import IntegrityError
from models.user import User
from models.token import AuthToken
from models.site import Site
import os

def _retrieve_google_user(google_token):
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(google_token, requests.Request(), os.getenv("GOOGLE_JS_CLIENT_ID"))

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise Exception("That token was not issued by Google")

        return idinfo
    except:
        raise Exception("That token is invalid or expired")


class AuthEndpoint(Resource):
    """
    Routes defined for signing in users
    """
    @security(True)
    def get(self, user, token, **kwargs):
        """Base auth test endpoint that will retrieve  a user given a token"""
        # If you get this far in endpoints that have @security(True)
        # Then a Token and a User exist in the kwargs
        return {
            "user": user.to_dict(),
            "token": token.to_dict()
        }, 200
    
    @json_input(["google_token"])
    def post(self, fields, **kwargs):
        """
        This endpoint signs in users with a google_token field.
        
        If the user's email exists, the existing user object will be returned
        If the user's email does not exist, a new User will be saved
        
        Either way, a new token will be issued
        """

        try:
            # Validate the google_token passed in (retrieves google user)
            g_user = _retrieve_google_user(fields["google_token"])

        except Exception as e:
            # Handle exceptions
            return {
                "message": str(e)
            }, 400
        
        # Make a new User
        new_user = User(
            email=g_user["email"],
            name=g_user["name"],
            given_name=g_user["given_name"],
            family_name=g_user["family_name"],
            google_id=g_user["sub"]
        )

        is_new_user = True

        try:
            # Save the new user to the DB
            new_user.save()
            user = new_user

        except IntegrityError:
            # That user already exists, rollback
            db.session().rollback()
            is_new_user = False

            # Find existing user
            existing_user = User.query.filter_by(email=new_user.email).first()
            user = existing_user
            pass

        # Send back a new auth token
        # TODO: Should we be invalidating old tokens here?
        new_token = AuthToken(user_id=user.id)
        new_token.save()
        token = new_token

        return_payload = {
            "user": user.to_dict(),
            "token": token.to_dict()
        }
        status_code = 200

        # TODO: This post method is doing too much and should be separated
        # Create a user's first site
        if is_new_user:
            status_code = 201
            new_site = Site(user_id=user.id)
            new_site.set_first_handle(user.name)
            return_payload["site"] = new_site.to_dict()

        return return_payload, status_code
