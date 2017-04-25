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
        # TODO: Cache the result of this puppy in Redis
        return HTML_from_markdown(
            self.content, extensions=["fenced_code"]
        )

    def increment_count(self, key, factor=1):
        if key == "love":
            self.love_count += factor
        elif key == "read":
            self.read_count += factor

    def increment_love_count(self, factor=1):
        self.increment_count("love", factor)

    def increment_read_count(self, factor=1):
        self.increment_count("read", factor)
