from django.test import TestCase
from django.contrib.auth.models import User
from django.http import HttpRequest


class ProjectsTests(TestCase):
    def test_url_projects_add(self):
      response = self.client.get('/projects/add/')
      self.assertEqual(response.status_code, 200)
    

            

    
     