from app import db
from sqlalchemy.dialects.postgresql import JSON

from helpers.cache import invalidate as invalidate_cached

from datetime import datetime
from uuid import UUID

import json
import os
import requests


class Base(db.Model):
    """
    Base Document for all model-level abstractions
    """
    created = DateTimeField(default=datetime.now)
    updated = DateTimeField(default=datetime.now)
    location = PointField()
    location_friendly = StringField()
    love_count = IntField(default=0)

    meta = {
        "abstract": True
    }

    # MARK - Private methods

    def _was_updated(self):
        # Changes the updated field to the current timestamp
        self.updated = datetime.now()

    def _fetch_friendly_location(self):
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", None)

        # Check to make sure we have a key
        if GOOGLE_API_KEY is None:
            return

        # Check that this call is necessary
        if self.location is None or self.location_friendly is not None:
            return

        loc_resp = requests.get(
            "https://maps.googleapis.com/maps/api/geocode/json?"
            "latlng={},{}&key={}".format(
                self.location[0],
                self.location[1],
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

        self.location_friendly = locality_comps[0]["long_name"]

    # MARK - Public methods

    def update_fields(self, updates):
        # NOTE: Not the most safe function (Reference fields etc...)
        for key, value in updates.items():
            if key in self._fields.keys():
                setattr(self, key, value)

    def save(self, *args, **kwargs):
        # Runs some tasks that always have to be run when saved
        self._was_updated()

        if self.location is not None and self.location_friendly is None:
            self._fetch_friendly_location()

        # Invalidate cached objects
        invalidate_cached(self._get_collection_name())

        # Run normal mongoengine save method
        super(Base, self).save(*args, **kwargs)

    def increment_love_count(self, factor=1):
        # Increments the love counter when an object is loved
        self.love_count += factor

    def delete(self, *args, **kwargs):
        # Runs some tasks that always have to be run when saved
        self._was_updated()

        # Invalidate cached objects
        invalidate_cached(self._get_collection_name())

        # Run normal mongoengine delete method
        super(Base, self).delete(*args, **kwargs)

    def to_dict(self, filters=[]):
        d = translate_bson_data_to_json_safe_data(self.to_mongo())

        if len(filters) > 0:
            filtered_keys = set(filters)

            for k in filtered_keys:
                if k in d:
                    del d[k]

        # Special mapping for outputting coordinates in a simpler way
        if "location" in d:
            d["location"] = d["location"]["coordinates"]

        return d

    def to_json(self, filters=[]):
        return json.dumps(self.to_dict(filters=filters))
