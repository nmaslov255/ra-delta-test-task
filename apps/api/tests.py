from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from django.core.exceptions import ValidationError

from .utils import calculate_delivery_price, fetch_rub_exchange_rate
from .validators import raise_for_invalide_name
from .tasks import calculate_delivery_prices

from .models import Package, PackageType


class TestApiUtils(TestCase):
    def test_calculate_delivery_price(self):
        self.assertEqual(calculate_delivery_price(200, 100, 70.5), 7050.0)

    def test_fetch_rub_exchange_rate(self):
        usd_price = fetch_rub_exchange_rate('USD')
        self.assertIsInstance(usd_price, float)
        self.assertTrue(usd_price > 0)


class TestApiValidators(TestCase):
    def test_raise_for_invalide_name(self):
        self.assertIsNone(raise_for_invalide_name('Valide name'))

        with self.assertRaises(ValidationError):
            raise_for_invalide_name('Invalide chars?!@#$%...')


class TestApiCelaryTasks(APITestCase):
    def setUp(self):
        self.url = '/api/package/'
        self.data = {
            "name": "test",
            "weight": 20,
            "price": 100,
            "package_type": 1
        }

    def test_calculate_delivery_prices(self):
        response = self.client.post(self.url, self.data)

        self.assertEqual(Package.objects.count(), 1)
        self.assertIsNone(Package.objects.get().delivery_price)
        self.assertIsNone(calculate_delivery_prices())
        self.assertIsNotNone(Package.objects.get().delivery_price)

class TestApiPackage(APITestCase):
    def setUp(self):
        self.url = '/api/package/'
        self.data = {
            "name": "test",
            "weight": 20,
            "price": 100,
            "package_type": 1
        }

    def test_create_package(self):
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_package = response.json()
        self.assertEqual(
            created_package.get('delivery_price'), 'Not calculated'
        )

class TestApiPackages(APITestCase):
    def test_get_packages(self):
        for idx in range(27):
            self.client.post('/api/package/', {
                'name': 'test',
                'weight': 1,
                'price': 1,
                'package_type': idx%3+1
            })

        path = '/api/packages/'
        response = self.client.get(f'{path}').json()
        self.assertEqual(len(response.get('results')), 10)

        response = self.client.get(f'{path}?page_size=5').json()
        self.assertEqual(len(response.get('results')), 5)

        response = self.client.get(f'{path}?page=3').json()
        self.assertEqual(len(response.get('results')), 7)

        response = self.client.get(f'{path}?package_type_id=1').json()
        self.assertEqual(len(response.get('results')), 9)

        type_id = PackageType.objects.first()
        Package.objects.filter(package_type=type_id).update(delivery_price=5)
        response = self.client.get(f'{path}?is_processed=1').json()
        self.assertEqual(len(response.get('results')), 9)

        response = self.client.get(f'{path}?is_processed=1').json()
        self.assertEqual(len(response.get('results')), 9)
