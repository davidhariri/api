from helpers.db import db
from models.base import Base
from models.user import User
from slugify import slugify
from sqlalchemy.exc import IntegrityError


class Site(Base):
    """
    The model for a Site object
    """
    __tablename__ = "sites"

    handle = db.Column(db.String(), unique=True, nullable=False)
    user_id = db.Column(db.ForeignKey(User.id), nullable=False)

    def set_first_handle(self, unsanitizied_str):
        self.handle = slugify(unsanitizied_str)

        try:
            self.save()
        except IntegrityError:
            # That handle already exists, rollback
            db.session().rollback()

            # Find existing sites that begin with that handle
            # NOTE: This query can be optimized:
            #   https://gist.github.com/hest/8798884
            existing_site_count = Site.query.filter(
                Site.handle.startswith(self.handle)).count()

            self.handle += "-{}".format(existing_site_count+1)

            return self.set_first_handle(self.handle)

        return self.handle

    def __repr__(self):
        return "<Site {}>".format(self.handle)
