from mongoengine.fields import (
    StringField,
    BooleanField,
    ListField
)
import re
import random
from markdown import markdown as HTML_from_markdown

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


class Note(Base):
    text = StringField(min_length=0, required=True, default="")
    description = StringField(default="")
    html = StringField(default="")
    public = BooleanField(default=True)
    slug = StringField(
        max_length=256,
        unique=True,
        required=True,
        default=_random_string,
        min_length=7
    )
    topics = ListField(field=StringField())

    meta = {
        "indexes": ["slug", "public", "text", "topics"]
    }

    # MARK - Private methods

    def _generate_html(self):
        self.html = HTML_from_markdown(
            self.text, extensions=["fenced_code"]
        )

    def _generate_description(self, word_count=50):
        description = re.sub("<[^<]+?>", "", self.html)

        if len(description) > 320:
            description = " ".join(
                description.split(" ")[:word_count]
            ) + "..."

        self.description = description

    # MARK - Public methods

    def save(self, *args, **kwargs):
        # Runs some tasks that always have to be run when saved
        self._generate_html()
        self._generate_description()

        self.validate()

        # Run normal mongoengine save method without validation
        super(Note, self).save(validate=False, *args, **kwargs)
