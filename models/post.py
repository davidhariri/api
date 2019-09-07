from helpers.db import db
import random
from sqlalchemy.dialects.postgresql import ARRAY
from models.base import Base
from models.user import User
from models.site import Site
import os
import requests

_SHARE_CHARS = (
    "abcdefghijklmnopqrstuvwxyz"
    "1234567890"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
)


def _make_slug(length=7):
    _ = ""

    for i in range(length):
        _ += random.choice(_SHARE_CHARS)

    return _


class Post(Base):
    """
    General Post
    """

    __tablename__ = "posts"

    slug = db.Column(db.String, nullable=False, unique=True, default=_make_slug)
    comment = db.Column(db.String)
    public = db.Column(db.Boolean, nullable=False, default=False)
    location_lat = db.Column(db.Float)
    location_lon = db.Column(db.Float)
    location_name = db.Column(db.String)
    review = db.Column(db.Integer)
    link_name = db.Column(db.String)
    link_uri = db.Column(db.String)
    love_count = db.Column(db.Integer, default=0)
    media = db.Column(ARRAY(db.String, dimensions=1))
    topics = db.Column(ARRAY(db.String, dimensions=1))
    tweet_id = db.Column(db.String)
    user_id = db.Column(db.ForeignKey(User.id), nullable=False)
    site_id = db.Column(db.ForeignKey(Site.id), nullable=False)

    def _fetch_friendly_location(self):
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", None)

        # Check to make sure we have a key
        if GOOGLE_API_KEY is None:
            return

        # Check that this call is necessary
        if self.location_lat is None or self.location_lon is None:
            return

        loc_resp = requests.get(
            "https://maps.googleapis.com/maps/api/geocode/json?"
            "latlng={},{}&key={}".format(
                self.location_lat,
                self.location_lon,
                GOOGLE_API_KEY
            )
        ).json()

        # Check for valid results
        if len(loc_resp["results"]) == 0:
            return

        address_comps = loc_resp["results"][0]["address_components"]
        locality_comps = list(filter(
            lambda ac: "locality" in ac["types"],
            address_comps
        ))

        if len(locality_comps) == 0:
            return

        self.location_name = locality_comps[0]["long_name"]

    def increment_love_count(self, factor=1):
        # Increments the love counter when an object is loved
        self.love_count += factor
