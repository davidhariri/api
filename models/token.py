import uuid
from mongoengine.fields import UUIDField
from models.base import Base


class AuthToken(Base):
    """
    Authorization tokens
    """
    token = UUIDField(required=True, default=uuid.uuid4)

    meta = {
        "indexes": ["token"]
    }
