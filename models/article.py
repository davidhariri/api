from mongoengine.fields import (
    StringField,
    BooleanField,
    IntField
)
import re
import random
from markdown import markdown as HTML_from_markdown
from slugify import slugify
from helpers.cache import invalidate as invalidate_cached

from models.base import Base

_SHARE_CHARS = (
    "abcdefghijklmnopqrstuvwxyz"
    "1234567890"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
)


def _random_string(l=7):
    _ = ""

    for i in range(l):
        _ += random.choice(_SHARE_CHARS)

    return _


class Article(Base):
    _SLUG_FIELDS = {
        "unique": True,
        "default": None,
        "sparse": True,
        "min_length": 1
    }

    title = StringField(max_length=512, min_length=0, required=True, default="")
    content = StringField(min_length=0, required=True, default="")
    html_content = StringField(default="")
    published = BooleanField(default=False)
    shared = BooleanField(default=False)
    love_count = IntField(default=0)
    read_count = IntField(default=0)
    description = StringField(default="")
    slug = StringField(max_length=256, **_SLUG_FIELDS)
    share_slug = StringField(max_length=7, **_SLUG_FIELDS)

    meta = {
        "indexes": ["slug", "share_slug", "published"]
    }

    # MARK - Private methods

    def _generate_html(self):
        self.html_content = HTML_from_markdown(
            self.content, extensions=["fenced_code"]
        )

    def _increment_count(self, key, factor):
        if key == "love":
            self.love_count += factor
        elif key == "read":
            self.read_count += factor

    def _generate_slug(self):
        """
        Generate the unique, URL-safe "slug" (human-friendly identifier)
        """
        self.slug = slugify(self.title)[:256]

    def _generate_share_slug(self):
        self.share_slug = _random_string()

    def _generate_description(self, word_count=50):
        description = re.sub("<[^<]+?>", "", self.html_content)

        if len(description) > 320:
            description = " ".join(
                description.split(" ")[:word_count]
            ) + "..."

        self.description = description

    # MARK - Public methods

    def increment_love_count(self, factor=1):
        # Increments the love counter when an Article is loved
        self._increment_count("love", factor)

    def increment_read_count(self, factor=1):
        # Increments the read counter when an Article is read
        self._increment_count("read", factor)

    def save(self, *args, **kwargs):
        # Runs some tasks that always have to be run when saved
        if self.published and self.slug is None:
            self._generate_slug()

        if self.shared and self.share_slug is None:
            self._generate_share_slug()

        self._generate_html()
        self._generate_description()

        self.validate()

        invalidate_cached("articles")

        # Run normal mongoengine save method
        super(Article, self).save(validate=False, *args, **kwargs)
