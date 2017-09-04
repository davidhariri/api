from base_test import BaseTest

from models.note import Note


class TestNote(BaseTest):
    def test_render_html(self):
        """
        Tests that render_html returns valid HTML
        """
        self.test_note.text = "# Test"
        self.test_note._generate_html()
        self.assertEquals(
            self.test_note.html, "<h1>Test</h1>")

    def test_increment_love_count_default(self):
        """
        Tests that increment_love_count increments the love_count by 1
        by default
        """
        self.test_note.increment_love_count()
        self.test_note.save()
        self.assertEquals(self.test_note.love_count, 1)

    def test_increment_love_count_custom(self):
        """
        Tests that increment_love_count increments the love_count by
        our custom factor
        """
        self.test_note.increment_love_count(9)
        self.test_note.save()
        self.assertEquals(self.test_note.love_count, 9)

    def test_generate_description_short(self):
        """
        Tests that a short note has a description with no
        trailing '...'
        """
        self.test_note.text = "# Hello World 👋"
        self.test_note.save()
        self.assertEquals(
            self.test_note.description, "Hello World 👋"
        )

    def test_generate_description_long(self):
        """
        Tests that a long note has a description with a
        trailing '...'
        """
        self.test_note.text = "word " * 100
        self.test_note.save()
        self.assertEquals(
            self.test_note.description, ("word " * 50)[:-1] + "..."
        )

    def test_save_empty_note(self):
        """
        Tests that an note can be created without text
        """
        self.test_note.text = ""
        self.test_note.save()

    def test_generate_share_handle(self):
        """
        Tests that the Note slug generator works
        """
        self.assertEquals(
            len(self.test_note.slug),
            7
        )

    def test_friendly_name_generation(self):
        """
        Tests that Notes that are given a valid location pair find
        a friendly location name
        """
        self.test_note = Note(location=[43.666674, -79.333167])
        self.test_note.save()
        self.assertEquals(self.test_note.location_friendly, "Toronto")

    def test_making_note_with_topics(self):
        """
        Tests that a Note can be made with topics
        """
        self.test_note = Note(topics=["topic", "topic2"])
        self.test_note.save()
        self.assertEquals(self.test_note.topics[0], "topic")

    def test_topic_note_dictionary(self):
        """
        Tests that a Notes dictionary represenation renders correctly
        """
        self.test_note = Note(topics=["topic"])
        self.test_note.save()
        d = self.test_note.to_dict()
        self.assertEquals(d["topics"], ["topic"])

    def test_friendly_name_generation_when_no_location(self):
        """
        Tests that Notes that are not given a friendly location string
        when they have no location
        """
        self.assertEquals(self.test_note.location_friendly, None)
