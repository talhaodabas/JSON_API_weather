import unittest

from main import (
    get_coordinates_city,
)


class TestGetCoordinates(unittest.TestCase):
    def test_gc_valid_search(self):
        result = get_coordinates_city("Trabzon")
        self.assertEqual(result, "Trabzon")

if __name__ == "__main__":
    unittest.main(verbosity=2)