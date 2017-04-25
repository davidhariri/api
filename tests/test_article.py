from base_test import BaseTest


class TestArticle(BaseTest):
    def test_render_html(self):
        """
        Tests that render_html returns valid HTML
        """
        self.simple_article.content = "# Test"
        html = self.simple_article.render_html()
        self.assertEquals(html, "<h1>Test</h1>")
