from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class SecurityTests(APITestCase):
    def test_api_root_requires_auth(self):
        url = reverse('usuario-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)