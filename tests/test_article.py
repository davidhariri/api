from base_test import BaseTest


class TestArticle(BaseTest):
    def test_render_html(self):
        """
        Tests that render_html returns valid HTML
        """
        self.simple_article.content = "# Test"
        html = self.simple_article.render_html()
        self.assertEquals(html, "<h1>Test</h1>")

    def test_increment_love_count_default(self):
        """
        Tests that increment_love_count increments the love_count by 1
        by default
        """
        self.simple_article.increment_love_count()
        self.simple_article.was_updated()
        self.simple_article.save()
        self.assertEquals(self.simple_article.love_count, 1)

    def test_increment_love_count_custom(self):
        """
        Tests that increment_love_count increments the love_count by
        our custom factor
        """
        self.simple_article.increment_love_count(9)
        self.simple_article.was_updated()
        self.simple_article.save()
        self.assertEquals(self.simple_article.love_count, 9)

    def test_increment_read_count_default(self):
        """
        Tests that increment_love_count increments the read_count by 1
        by default
        """
        self.simple_article.increment_read_count()
        self.simple_article.was_updated()
        self.simple_article.save()
        self.assertEquals(self.simple_article.read_count, 1)

    def test_increment_read_count_custom(self):
        """
        Tests that increment_read_count increments the read_count by
        our custom factor
        """
        self.simple_article.increment_read_count(9)
        self.simple_article.was_updated()
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
            self.simple_article.generate_slug()
            self.simple_article.save()
            self.assertEquals(self.simple_article.slug, t[1])