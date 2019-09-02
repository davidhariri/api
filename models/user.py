from helpers.db import db
import re
import random
from models.base import Base


class User(Base):
    """
    User class
    """

    __tablename__ = "users"

    email = db.Column(db.String(254), unique=True, nullable=False)
    name = db.Column(db.String())
    given_name = db.Column(db.String())
    family_name = db.Column(db.String())
    google_id = db.Column(db.String())

    def __repr__(self):
        return "<User {}>".format(self.email)
