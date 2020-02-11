from django.contrib.auth.models import User
from django_dynamic_fixture import G
from rest_framework.test import APIClient

from users.models import Profile


class DefaultUserTest:

    def __init__(self):
        self.create_authenticated_user()
        self.create_401_user()

    def create_authenticated_user(self):
        self.client = APIClient()
        self.user = G(User)
        self.user.set_password("testapipairgame**.")
        self.user.save()
        G(Profile, user=self.user)
        self.client.login(username=self.user.username, password="testapipairgame**.")

    def create_401_user(self):
        self.client_unauthenticated = APIClient()
