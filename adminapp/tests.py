from django.conf import settings
from django.test import TestCase
from django.test.client import Client

from userapp.models import User
from userapp.views import get_sha1


class TestAdminappSmoke(TestCase):
    fixtures = [
        "mainapp/fixtures/001_categories.json",
        "mainapp/fixtures/002_products.json",
        "mainapp/fixtures/admin_user.json",
    ]

    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create_superuser("django2", "django2@geekshop.local", "geekbrains")
        self.user = User.objects.create_user("petya", "petya@geekbrains.ru", "123456")

    def test_user_login(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["user"].is_anonymous)
        self.assertEqual(response.context["title"], "GeekShop. главная")
        self.assertNotContains(response, "Пользователь", status_code=200)

        # Log in
        response = self.client.get("/user/login/")
        self.assertEqual(response.status_code, 200)

        # Set user's data
        self.client.login(username="petya", password="123456")

        # Log in
        response = self.client.get("/user/login/")
        self.assertEqual(response.status_code, 302)

        # After log in
        response = self.client.get("/")
        self.assertFalse(response.context["user"].is_anonymous)
        self.assertEqual(response.context["user"], self.user)
        self.assertContains(response, "ПРОФИЛЬ", status_code=200)

    def test_superuser_login(self):
        self.client.login(username='django2', password='geekbrains')

        response = self.client.get('/user/profile/')
        self.assertEqual(response.context['user'].is_superuser, True)

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('АДМИНКА', response.content.decode())

    def test_profile_login_redirect(self):
        # Test without log in. Must be redirect.
        response = self.client.get("/user/profile/")
        self.assertEqual(response.url, "/user/login/?next=/user/profile/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username="petya", password="123456")

        response = self.client.get("/user/profile/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user"], self.user)
        self.assertEqual(response.context["title"], f"Профиль пользователя {self.user.username}")
        self.assertEqual(response.request["PATH_INFO"], "/user/profile/")

    def test_user_logout(self):
        # Log out for anonimous
        response = self.client.get("/user/logout/")
        self.assertEqual(response.status_code, 302)

        # Log in
        response = self.client.get("/user/login/")
        self.assertEqual(response.status_code, 200)

        # User's data
        self.client.login(username="petya", password="123456")

        # Log in
        response = self.client.get("/user/login/")
        self.assertEqual(response.status_code, 302)

        # Log out
        response = self.client.get("/user/logout/")
        self.assertEqual(response.status_code, 302)

        # After log out
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["user"].is_anonymous)
        self.assertEqual(response.context["title"], "GeekShop. главная")
        self.assertNotIn("ПРОФИЛЬ", response.content.decode())

    def test_user_register(self):
        response = self.client.get("/user/register/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["title"], "GeekShop - Регистрация")
        self.assertTrue(response.context["user"].is_anonymous)

        new_user_data = {
            "username": "samuel",
            "first_name": "Сэмюэл",
            "last_name": "Джексон",
            "password1": "geekbrains",
            "password2": "geekbrains",
            "email": "sumuel@geekshop.local",
            "age": "21",
        }

        # Create new user
        response = self.client.post("/user/register/", data=new_user_data)
        self.assertEqual(response.status_code, 302)

        new_user = User.objects.get(username=new_user_data["username"])
        # print(new_user, new_user.activation_key)

        activation_url = f"{settings.DOMAIN_NAME}/user/verify/?user={new_user.id}&hash={get_sha1(new_user.email)}&key={new_user.activation_key}"
        # print(activation_url)

        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, 200)

        # Log in
        response = self.client.get("/user/login/")
        self.assertEqual(response.status_code, 302)

        # self.client.login(username=new_user_data["username"], password=new_user_data["password1"])

        # Log in
        response = self.client.get("/user/profile/")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["user"].is_anonymous)
        self.assertContains(response, text=new_user_data["first_name"], status_code=200)

        # Main page check
        response = self.client.get("/")
        self.assertContains(response, 'ПРОФИЛЬ', status_code=200)
