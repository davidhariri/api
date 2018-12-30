from helpers.db import db
import uuid
from sqlalchemy.dialects.postgresql import UUID


class AuthToken(db.Model):
	"""
	Authorization tokens

	TODO: Index on token
	"""
	__tablename__ = 'tokens'

	token = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False, unique=True)

