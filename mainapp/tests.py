from django.test import TestCase
from django.test.client import Client

from mainapp.models import Product, ProductCategory


class TestMainappSmoke(TestCase):
    fixtures = [
        "mainapp/fixtures/001_categories.json",
        "mainapp/fixtures/002_products.json",
        "mainapp/fixtures/admin_user.json",
    ]

    def setUp(self):
        self.client = Client()

    def test_fixtures_load(self):
        # Check fixtures loading
        self.assertGreater(ProductCategory.objects.count(), 0)
        self.assertGreater(Product.objects.count(), 0)

    def test_mainapp_urls(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/products/5/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/products/7/")
        self.assertEqual(response.status_code, 200)

        for category in ProductCategory.objects.all():
            response = self.client.get(f"/products/{category.pk}/")
            self.assertEqual(response.status_code, 200)

    def test_mainapp_json_requests(self):
        for product in Product.objects.all():
            response = self.client.post(f"/products/info/{product.pk}/", {}, **{'HTTP_X_REQUESTED_WITH':
                                                                                    'XMLHttpRequest'})
            self.assertEqual(response.status_code, 200)


class ProductsTestCase(TestCase):
    fixtures = [
        "mainapp/fixtures/001_categories.json",
        "mainapp/fixtures/002_products.json",
        "mainapp/fixtures/admin_user.json",
    ]

    def test_product_print(self):
        product_1 = Product.objects.get(name="Синяя куртка The North Face")
        product_2 = Product.objects.get(name="Черный рюкзак Nike Heritage")
        self.assertEqual(str(product_1), "21: Синяя куртка The North Face (Одежда)")
        self.assertEqual(str(product_2), "23: Черный рюкзак Nike Heritage (Аксессуары)")

    def test_product_get_items(self):
        product_1 = Product.objects.get(name="Синяя куртка The North Face")
        product_3 = Product.objects.get(name="Черный рюкзак Nike Heritage")

        products_as_class_method = set(product_1.get_items())
        products = set([product_1, product_3])

        self.assertIsNotNone(products_as_class_method.intersection(products))
