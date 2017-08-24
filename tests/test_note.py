from base_test import BaseTest


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
