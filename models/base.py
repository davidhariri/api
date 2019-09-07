from helpers.db import db
from uuid import UUID
from enum import Enum
from datetime import datetime
import json


def translate_model_data_to_json_safe_data(pg_data):
    if isinstance(pg_data, datetime):
        pg_data = pg_data.isoformat()

    elif isinstance(pg_data, UUID):
        pg_data = str(pg_data)

    elif isinstance(pg_data, Enum):
        pg_data = pg_data.value

    elif isinstance(pg_data, dict):
        for key in pg_data:
            pg_data[key] = translate_model_data_to_json_safe_data(
                pg_data[key])

    elif isinstance(pg_data, list):
        for index, value in enumerate(pg_data):
            pg_data[index] = translate_model_data_to_json_safe_data(
                value)

    return pg_data


class Base(db.Model):
    """
    General abstractions for all models
    """

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.now())
    date_updated = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def to_dict(self, filters=[]):
        _d = {}

        for column in self.__table__.columns:
            _d[column.name] = getattr(self, column.name)

        d = translate_model_data_to_json_safe_data(_d)

        if len(filters) > 0:
            filtered_keys = set(filters)

            for k in filtered_keys:
                if k in d:
                    del d[k]

        return d

    def to_json(self, filters=[]):
        return json.dumps(self.to_dict(filters=filters))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
