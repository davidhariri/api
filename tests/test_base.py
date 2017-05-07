from models.base import Base

from base_test import BaseTest


class TestBase(BaseTest):
    def test_was_updated_updates_updated(self):
        """
        Tests that Base.was_updated() changes the user's updated field
        """
        base = Base()

        self.assertEquals(
            round(base.created.timestamp(), 3),
            round(base.updated.timestamp(), 3))

        base._was_updated()
        self.assertFalse(base.created == base.updated)
