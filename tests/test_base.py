import unittest
from mongoengine import connect

from models.base import Base


class BaseTest(unittest.TestCase):
    """
    Convenience object that encapsulates basic test case set up
    like creating a test user and organization as well as tearing
    down the database etc...
    """
    def set_up_database(self):
        # Create the plusequals-test database
        self.db = connect("dhariri-test")
        self.base = Base()

    def setUp(self):
        # Set up the database
        self.set_up_database()

    def tearDown(self):
        # Drop all collections
        self.db.drop_database("dhariri-test")

    # MARK - Begin Base tests

    def test_was_updated_updates_updated(self):
        """
        Tests that Base.was_updated() changes the user's updated field
        """
        self.assertEquals(
            round(self.base.created.timestamp(), 3),
            round(self.base.updated.timestamp(), 3))

        self.base.was_updated()
        self.assertFalse(self.base.created == self.base.updated)
