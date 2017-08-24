import unittest
from mongoengine import connect

from models.article import Article


class BaseTest(unittest.TestCase):
    """
    Convenience object that encapsulates basic test case set up
    like creating a test user and organization as well as tearing
    down the database etc...
    """
    def set_up_database(self):
        # Create the plusequals-test database
        self.db = connect("dhariri-test")

    def setUp(self):
        # Set up the database
        self.set_up_database()

        self.simple_article = Article(
            title="My New Article",
            content="# Hello World 🏄")

        self.simple_article.save()

    def tearDown(self):
        # Drop all collections
        self.db.drop_database("dhariri-test")
