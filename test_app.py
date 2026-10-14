
import unittest
from app import calculate_total, service_status


class TestApplication(unittest.TestCase):

    def test_calculate_total(self):
        self.assertEqual(calculate_total(10, 3), 30)

    def test_reject_negative_price(self):
        with self.assertRaises(ValueError):
            calculate_total(-1, 2)

    def test_service_status(self):
        self.assertEqual(service_status()["status"], "healthy")



if __name__ == "__main__":
    unittest.main(verbosity=2)
