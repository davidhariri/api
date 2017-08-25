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

    def test_location_generated_as_lat_lon_array_in_json(self):
        """
        Tests that when a Base object is rendered as json it returns
        a nicely formatted tuple (list) of Floats
        """
        test_loc = [42.73658, -27.457975]
        test_obj = Base(location=test_loc)
        test_obj_json = test_obj.to_dict()
        self.assertEquals(test_obj_json["location"], test_loc)
