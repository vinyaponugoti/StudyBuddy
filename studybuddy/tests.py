from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.

class LoginTestCase(TestCase):


    def login_test(self):
        user = User.objects.create(username='test_acc')
        user.set_password('12345')
        user.is_active = True
        user.save()

        self.client.login(username='test_acc', password='12345')

        response = self.flow()

        self.assertEqual(200, response.status_code, response.content)
        self.assertContains(response, 'This profile is already connected to another user account')

