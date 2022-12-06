from django.contrib.auth.models import User
from .models import LutherClass, StudySession, StudyPost, PostRequest, ScheduleClass, Profile
from django.test import TestCase
from django.test import Client
from .forms import ScheduleForm

class LoginTestCase(TestCase):
     def test_login(self):
       # user = User.objects.create(username='test_acc')
       # user.set_password('12345')
       # user.is_active = True
       # user.save()
       #
       # self.client.login(username='test_acc', password='12345')
       #
       # response = self.flow()

       c = Client()

       response = c.post('/login', {'username': 'admin', 'password': 'admin'})

       self.assertEqual(301, response.status_code)
class URLTestCases(TestCase):
      #tests to see that all urls will not return an 404 error.

      def test_login(self):
          response = self.client.get('/accounts/login/')
          self.assertEqual(response.status_code, 301)

      def test_google_website(self):
          response = self.client.get('/accounts/google/login/')
          self.assertEqual(response.status_code, 301)

      def test_search(self):
          response = self.client.get('/search')
          self.assertEqual(response.status_code, 301)

class Functionality_Tests(TestCase):

      def test_valid_schedule_form(self):
         response = self.client.post("/editschedule", data = {
                                                             "class_department" : "CS",
                                                             "class" : "1110"})

         self.assertEquals(response.status_code, 301)

      def test_invalid_schedule_form(self):
         response = self.client.post("/editschedule", data={
             "class_department": "CS",
            "class": "1115"})

         self.assertEqual(response.status_code, 301)




