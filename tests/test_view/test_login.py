from django.contrib.auth.models import User
from django.test import tag
from django.urls import reverse
from rest_framework.test import APITestCase


@tag("restapi", "auth_route", "login")
class TestLogin(APITestCase):
    def setUp(self):
        super(TestLogin, self).setUp()

    login_url = reverse("api:auth:login")

    # logout_url = reverse("api:v1:users:logout")

    def test_can_login_new_user(self):
        response = self.client.post(self.login_url, data={"email": "test@test.com", "password": "test"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"email": "test@test.com"})
        User.objects.get(username="test@test.com")

    def test_can_login_old_user(self):
        self.client.post(self.login_url, data={"email": "test@test.com", "password": "test"}, format="json")
        response = self.client.post(self.login_url, data={"email": "test@test.com", "password": "test"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"email": "test@test.com"})
        User.objects.get(username="test@test.com")
