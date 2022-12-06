from django.contrib.auth.models import User
from django.test import TestCase

#Create your tests here.
class LoginTestCase(TestCase):
    def test_login(self):
      user = User.objects.create(username='test_acc')
      user.set_password('12345')
      user.is_active = True
      user.save()

      self.client.login(username='test_acc', password='12345')

      response = self.flow()

      self.assertEqual(200, response.status_code, response.content)
      self.assertContains(response, 'This profile is already connected to another user account')
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


class Functionality_Tests(TestCase):
    # def test_add_class(self):
    #     test_user = Profile.objects.filter(user='jim')
    #
    #     luther_list = LutherClass.objects.all()
    #     classes = ScheduleClass.objects.all(test_user)
    #     course_list = {}
    #
    #     schedule_form = ScheduleForm()
    #     updated_classes = Profile.get_classes(test_user)
    #     context = {
    #             "schedule_form": schedule_form,
    #             "classes": classes,
    #             "luther_list": luther_list,
    #             "updated_classes": updated_classes,
    #             "course_list": course_list
    #         }
    #
    #     response = self.client.get('/editschedule')
    #
    #     self.assertEquals(response.status_code, 200)


    def test_valid_schedule_form(self):
        response = self.client.post("/editschedule", data = {
                                                            "class_department" : "CS",
                                                            "class" : "1110"})

        self.assertEquals(response.status_code, 200)

    def test_invalid_schedule_form(self):
        response = self.client.post("/editschedule", data={
            "class_department": "CS",
            "class": "1110"})

        self.assertNotEqual(response.status_code, 200)





