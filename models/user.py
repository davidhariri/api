from helpers.db import db
import re
import random
from models.base import Base


class User(Base):
    """
    User class
    """

    __tablename__ = "users"

    email = db.Column(db.String(254), unique=True)
    name = db.String()
    given_name = db.String()
    family_name = db.String()
    google_id = db.String()

    def __repr__(self):
        return "<User {}>".format(self.id)
