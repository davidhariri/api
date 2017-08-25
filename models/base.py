from mongoengine import Document
from mongoengine.fields import (
    DateTimeField,
    PointField,
    IntField,
    StringField
)
from helpers.cache import invalidate as invalidate_cached

from datetime import datetime
from bson.objectid import ObjectId
from uuid import UUID

import json


def translate_bson_data_to_json_safe_data(bson_data):
    if isinstance(bson_data, ObjectId):
        bson_data = str(bson_data)

    elif isinstance(bson_data, datetime):
        bson_data = float(bson_data.strftime("%s.%f"))

    elif isinstance(bson_data, UUID):
        bson_data = str(bson_data)

    elif isinstance(bson_data, dict):
        for key in bson_data:
            bson_data[key] = translate_bson_data_to_json_safe_data(
                bson_data[key])

    elif isinstance(bson_data, list):
        for index, value in enumerate(bson_data):
            bson_data[index] = translate_bson_data_to_json_safe_data(
                value)

    return bson_data


class Base(Document):
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
        # FIXME: Google API Call here
        self.location_friendly = "Toronto"

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
