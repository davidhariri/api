from helpers.db import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from models.base import Base 
from models.user import User


class AuthToken(Base):
    """
    Authorization tokens
    """
    __tablename__ = "tokens"

    token = db.Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False, unique=True)
    user_id = db.Column(db.ForeignKey(User.id), nullable=False)

    def __repr__(self):
        return "<Token {}>".format(self.token)

