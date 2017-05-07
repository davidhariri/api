from mongoengine import Document
from mongoengine.fields import DateTimeField

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

    meta = {
        "abstract": True
    }

    # MARK - Private methods

    def _was_updated(self):
        # Changes the updated field to the current timestamp
        self.updated = datetime.now()

    # MARK - Public methods

    def save(self, *args, **kwargs):
        # Runs some tasks that always have to be run when saved
        self._was_updated()

        # Run normal mongoengine save method
        super(Base, self).save(*args, **kwargs)

    def to_dict(self, filters=[]):
        d = translate_bson_data_to_json_safe_data(self.to_mongo())

        if len(filters) > 0:
            filtered_keys = set(filters)

            for k in filtered_keys:
                del d[k]

        return d

    def to_json(self, filters=[]):
        return json.dumps(self.to_dict(filters=filters))
