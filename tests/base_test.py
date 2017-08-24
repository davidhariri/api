import unittest
from mongoengine import connect

from models.note import Note


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
        self.test_note = Note(text="# Hello World! 🏄")
        self.test_note.save()

    def tearDown(self):
        # Drop all collections
        self.db.drop_database("dhariri-test")
