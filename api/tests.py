from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status

User = get_user_model()


class BookAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_book_list_authenticated(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_book_create(self):
        data = {"title": "Test Book", "author": "Test Author", "isbn": "1234567890123"}
        response = self.client.post('/api/books/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AdminUserTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='adminpass123', is_admin=True)
        self.token = Token.objects.create(user=self.admin_user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_admin_can_create_book(self):
        data = {"title": "Admin Book", "author": "Admin Author", "isbn": "9876543210123"}
        response = self.client.post('/api/books/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class RegularUserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='regular', password='regularpass123')
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_regular_user_cannot_create_book(self):
        data = {"title": "User Book", "author": "User Author", "isbn": "1122334455667"}
        response = self.client.post('/api/books/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
