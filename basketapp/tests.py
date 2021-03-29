from django.test import TestCase
from django.test.client import Client

from userapp.models import User
from mainapp.models import Product
from basketapp.models import Basket


class TestBasketappSmoke(TestCase):
    fixtures = [
        "mainapp/fixtures/001_categories.json",
        "mainapp/fixtures/002_products.json",
        "mainapp/fixtures/admin_user.json",
    ]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user("petya", "petya@geekbrains.ru", "123456")

    def test_basket(self):
        # Check urls
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["user"].is_anonymous)

        # Add to basket with anonimous
        response = self.client.get("/basket/add/21/")
        self.assertEqual(response.url, "/user/login/?next=/basket/add/21/")
        self.assertEqual(response.status_code, 302)

        # login
        self.client.login(username="petya", password="123456")

        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["user"].is_anonymous)

        # Add to basket
        response = self.client.get("/basket/add/21/")
        self.assertEqual(response.status_code, 302)

        # Change count
        basket = Basket.objects.filter(user_id=self.user.id).first()
        self.assertEqual(basket.quantity, 1)
        response = self.client.post(f'/basket/edit/{basket.id}/3/', {}, **{'HTTP_X_REQUESTED_WITH':
                                                                                'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)
        basket = Basket.objects.filter(user_id=self.user.id).first()
        self.assertEqual(basket.quantity, 3)

        # Change count
        product = Product.objects.get(id=basket.product.id)
        all_count = product.quantity + basket.quantity
        response = self.client.post(f'/basket/edit/{basket.id}/{all_count * 2}/', {}, **{'HTTP_X_REQUESTED_WITH':
                                                                                'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)
        basket = Basket.objects.filter(user_id=self.user.id).first()
        self.assertEqual(basket.quantity, all_count)

        # Remove basket
        response = self.client.get(f"/basket/remove/{basket.id}/")
        self.assertEqual(response.status_code, 302)
        basket = Basket.objects.filter(user_id=self.user.id)
        self.assertEqual(len(basket), 0)
