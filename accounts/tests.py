from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

# Create your tests here.

class RegisterTestCase(APITestCase):

    def test_register(self):
        data = {
            "username" : "hello",
            "email" : "hello@gmail.com",
            "password" : "123",
            "password2" : "123"
        }

        reponse = self.client.post(reverse('register'),data)
        self.assertEqual(reponse.status_code, status.HTTP_201_CREATED)