import json

from django.test import TestCase
from django.urls import reverse
from django_dynamic_fixture import G
from rest_framework import status

from users.utils import DefaultUserTest
from worlds.models import World, Image


class WorldListAPITests(TestCase, DefaultUserTest):
    def setUp(self):
        DefaultUserTest.__init__(self)
        self.url = reverse("worlds:api_worlds")
        self.model = World
        for i in range(5):
            G(self.model)

    def test_unauthenticated(self):
        response = self.client_unauthenticated.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_all(self):
        response = self.client.get(self.url, format="json")
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result), self.model.objects.count())

    def test_filter_by_status(self):
        # With status equal to finished
        url = self.url + "?status=finished"
        response = self.client.get(url, format="json")
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result), 0)

        # With status equal to pending
        url = self.url + "?status=pending"
        response = self.client.get(url, format="json")
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result), self.model.objects.count())


class ImageListAPITests(TestCase, DefaultUserTest):
    def setUp(self):
        DefaultUserTest.__init__(self)
        self.url = reverse("worlds:api_images")
        self.model = Image
        for i in range(5):
            G(self.model)

    def test_list_all(self):
        response = self.client_unauthenticated.get(self.url, format="json")
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result), self.model.objects.count())

    def test_search_by_id(self):
        image = G(Image, id="idtest**.")
        url = self.url + "?search=" + image.id
        response = self.client_unauthenticated.get(url, format="json")
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result), 1)

    def test_search_by_title(self):
        image = G(Image, title="my test title **.")
        url = self.url + "?search=" + image.title
        response = self.client_unauthenticated.get(url, format="json")
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result), 1)

    def test_filter_by_world(self):
        world = G(World)
        G(Image, world=world)
        url = self.url + "?world=" + str(world.id)
        response = self.client_unauthenticated.get(url, format="json")
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result), 1)
