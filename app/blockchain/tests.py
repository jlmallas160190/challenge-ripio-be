from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class TestCoinViewSet(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test', password='test123')
        self.user.save()

    def test_list(self):
        self.client.login(username="test", password="test123")
        response = self.client.get('/api/v1/blockchain/coins/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
