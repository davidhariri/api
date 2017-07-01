from base_test import BaseTest


class TestArticle(BaseTest):
    def test_render_html(self):
        """
        Tests that render_html returns valid HTML
        """
        self.simple_article.content = "# Test"
        self.simple_article._generate_html()
        self.assertEquals(
            self.simple_article.html_content, "<h1>Test</h1>")

    def test_increment_love_count_default(self):
        """
        Tests that increment_love_count increments the love_count by 1
        by default
        """
        self.simple_article.increment_love_count()
        self.simple_article.save()
        self.assertEquals(self.simple_article.love_count, 1)

    def test_increment_love_count_custom(self):
        """
        Tests that increment_love_count increments the love_count by
        our custom factor
        """
        self.simple_article.increment_love_count(9)
        self.simple_article.save()
        self.assertEquals(self.simple_article.love_count, 9)

    def test_increment_read_count_default(self):
        """
        Tests that increment_love_count increments the read_count by 1
        by default
        """
        self.simple_article.increment_read_count()
        self.simple_article.save()
        self.assertEquals(self.simple_article.read_count, 1)

    def test_increment_read_count_custom(self):
        """
        Tests that increment_read_count increments the read_count by
        our custom factor
        """
        self.simple_article.increment_read_count(9)
        self.simple_article.save()
        self.assertEquals(self.simple_article.read_count, 9)

    def test_generate_slug(self):
        """
        Tests that various combinatons of words and characters generate
        url-safe slugs
        """
        titles = [
            (" Hello World", "hello-world"),
            (" 💪 My Siçk  Title", "my-sick-title"),
            ("M¥  cool 🌈 post 🐘  ", "my-cool-post"),
            ("    µy very ¬ong post title", "uy-very-ong-post-title"),
        ]

        for t in titles:
            self.simple_article.title = t[0]
            self.simple_article._generate_slug()
            self.simple_article.save()
            self.assertEquals(self.simple_article.slug, t[1])

    def test_generate_description_short(self):
        """
        Tests that a short article has a description with no
        trailing '...'
        """
        self.simple_article.content = "# Hello World 👋"
        self.simple_article.save()
        self.assertEquals(
            self.simple_article.description, "Hello World 👋"
        )

    def test_generate_description_long(self):
        """
        Tests that a long article has a description with a
        trailing '...'
        """
        self.simple_article.content = "word " * 100
        self.simple_article.save()
        self.assertEquals(
            self.simple_article.description, ("word " * 50)[:-1] + "..."
        )

    def test_save_empty_article(self):
        """
        Tests that an article can be created without a title or content
        which would be more like a note
        """
        self.simple_article.content = ""
        self.simple_article.title = ""
        self.simple_article.save()

    def test_generate_share_handle(self):
        """
        Tests that the Article share handle generator works
        """
        self.simple_article._generate_share_slug()
        self.assertEquals(
            len(self.simple_article.share_slug),
            7
        )
