from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.
# class LoginTestCase(TestCase):
#     def test_login(self):
#        user = User.objects.create(username='test_acc')
#         user.set_password('12345')
#         user.is_active = True
#         user.save()
#
#         self.client.login(username='test_acc', password='12345')
#
#         response = self.flow()
#
#         self.assertEqual(200, response.status_code, response.content)
#         self.assertContains(response, 'This profile is already connected to another user account')
class URLTestCases(TestCase):
    #tests to see that all urls will not return an 404 error.

    def test_login(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_google_website(self):
        response = self.client.get('/accounts/google/login/')
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        response = self.client.get('/search')
        self.assertEqual(response.status_code, 200)




