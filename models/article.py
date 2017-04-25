from mongoengine.fields import (
    StringField,
    BooleanField,
    IntField
)
from markdown import markdown as HTML_from_markdown

from models.base import Base


class Article(Base):
    title = StringField(max_length=512, min_length=1, required=True)
    content = StringField(min_length=1, required=True)
    published = BooleanField(default=False)
    shared = BooleanField(default=False)
    love_count = IntField(default=0)
    read_count = IntField(default=0)

    def render_html(self):
        # TODO: Cache the result of this puppy
        return HTML_from_markdown(
            self.content, extensions=["fenced_code"]
        )
