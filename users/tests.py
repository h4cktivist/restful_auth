from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
import json


class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        url = reverse('register')
        data = {"email": "test@example.com", "password": "password123"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.content)['user']['email'], "test@example.com")

    def test_register_bad_request(self):
        url = reverse('register')
        data = {"email": "test@example.com"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

        data = {"password": "password123"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_login_user(self):
        login_url = reverse('login')
        register_url = reverse('register')
        data = {"email": "test@example.com", "password": "password123"}
        register_response = self.client.post(register_url, data, format='json')
        login_response = self.client.post(login_url, data, format='json')
        self.assertEqual(login_response.status_code, 200)
        self.assertIn("access_token", login_response.data)
        self.assertIn("refresh_token", login_response.data)

    def test_login_wrong_credentials(self):
        login_url = reverse('login')
        register_url = reverse('register')
        data = {"email": "test@example.com", "password": "password123"}
        register_response = self.client.post(register_url, data, format='json')
        wrong_data = {"email": "test@example.com", "password": "password_wrong"}
        login_response = self.client.post(login_url, wrong_data, format='json')
        self.assertEqual(login_response.status_code, 401)

    def test_refresh_token(self):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")
        data = {"email": "test@example.com", "password": "password123"}
        login_response = self.client.post(reverse('login'), data, format='json')
        refresh_token = login_response.data['refresh_token']

        url = reverse('refresh')
        refresh_data = {"refresh_token": refresh_token}
        response = self.client.post(url, refresh_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)

        false_refresh_data = {"refresh_token": str(refresh_token)[::-1]}
        response = self.client.post(url, false_refresh_data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_logout_user(self):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")
        data = {"email": "test@example.com", "password": "password123"}
        login_response = self.client.post(reverse('login'), data, format='json')
        refresh_token = login_response.data['refresh_token']

        url = reverse('logout')
        logout_data = {"refresh_token": refresh_token}
        response = self.client.post(url, logout_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], "User logged out.")

        false_logout_data = {"refresh_token": str(refresh_token)[::-1]}
        response = self.client.post(url, false_logout_data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_get_user_profile(self):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")
        data = {"email": "test@example.com", "password": "password123"}
        login_response = self.client.post(reverse('login'), data, format='json')

        access_token = login_response.data['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        url = reverse('me')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.data)

    def test_get_user_profile_no_token(self):
        url = reverse('me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_update_user_profile(self):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")
        data = {"email": "test@example.com", "password": "password123"}
        login_response = self.client.post(reverse('login'), data, format='json')

        access_token = login_response.data['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        url = reverse('me')
        update_data = {"username": "new_username"}
        response = self.client.put(url, update_data, HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "new_username")

    def test_update_user_profile_no_token(self):
        url = reverse('me')
        update_data = {"username": "new_username"}
        response = self.client.put(url, update_data)
        self.assertEqual(response.status_code, 403)
