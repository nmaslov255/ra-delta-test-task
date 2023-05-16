from django.test import TestCase

from .utils import calculate_delivery_price


class TestApiUtils(TestCase):
    def test_calculate_delivery_price(self):
        self.assertEqual(calculate_delivery_price(200, 100, 70.5), 7050.0)
