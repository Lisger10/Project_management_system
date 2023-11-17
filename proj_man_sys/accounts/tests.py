from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AccountTest(TestCase):
    def test_url_login(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_url_login_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_url_signup(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)
    
    def test_url_signup_by_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200 )

    def test_template_name_correct(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response, '<h1>Вход</h1>')

    def test_template_name_correct(self):
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'registration/signup.html')