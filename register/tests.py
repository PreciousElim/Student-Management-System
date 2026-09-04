# from django.contrib.auth import get_user_model
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase

# from students.models import Student
# from courses.models import Course, Department
# from .models import Register

# User = get_user_model()


# class RegisterTests(APITestCase):

#     def setUp(self):
#         # A logged-in user to make authenticated requests
#         self.user = User.objects.create_user(
#             username='testuser',
#             password='testpass123'
#         )
#         self.client.force_authenticate(user=self.user)

#         # Shared department for all courses/students
#         self.department = Department.objects.create(
#             name='Computer Science',
#             )
#         self.department_1 = Department.objects.create(
#             name = 'Cyber Security'
#         )

#         # A 100 level student
#         self.student_100 = Student.objects.create(
#             first_name='Ada',
#             last_name='Lovelace',
#             matric_number='CSC001',
#             email='ada@example.com',
#             department=self.department,
#             level=100,
#             age=18
#         )
        
#         # A 300 level student
#         self.student_300 = Student.objects.create(
#             first_name='Jon',
#             last_name='Doe',
#             matric_number='CSC002',
#             email='jon@example.com',
#             department=self.department,
#             level=300,
#             age=20
#         )
#         # A 300 level student with a different department
#         self.student_300_1 = Student.objects.create(
#             first_name='Mee',
#             last_name='Ben',
#             matric_number='CSC003',
#             email='mee@example.com',
#             department=self.department_1,
#             level=300,
#             age=20
#         )
        
        
#         # An 100 level course
#         self.course_100 = Course.objects.create(
#             department=self.department,
#             course_code='CSC101',
#             course_title='Intro to Programming',
#             level=100,
#             semester='first',
#             course_unit=3
#         )

#         # A 300 level course(computer science)
#         self.course_300 = Course.objects.create(
#             department=self.department,
#             course_code='CSC301',
#             course_title='Advanced Algorithms',
#             level=300,
#             semester='first',
#             course_unit=3
#         )
#         # A 300 level course(cyber security)
#         self.course_300_1 = Course.objects.create(
#             department=self.department_1,
#             course_code='CYB301',
#             course_title= 'Network Security',
#             level=300,
#             semester='first',
#             course_unit=3
#         )
        
        
#     def test_successful_registration(self):
#         """A student can register for a course at their own level."""
#         url = reverse('register-list')
#         data = {
#             'student': self.student_100.id,
#             'course': self.course_100.id,
#             'session': '2025/2026'
#         }
#         response = self.client.post(url, data)

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Register.objects.count(), 1)
        
#     def test_carryover_level_mismatch_accepted(self):
#         """You can register a carry over course"""
#         url = reverse('register-list')
#         data = {
#             'student': self.student_300.id,
#             'course': self.course_100.id,
#             'session': '2025/2026'
#         }
#         response = self.client.post(url, data)
        
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Register.objects.count(), 1)

#     def test_level_mismatch_rejected(self):
#         """A 100 level student cannot register for a 300 level course."""
#         url = reverse('register-list')
#         data = {
#             'student': self.student_100.id,
#             'course': self.course_300.id,
#             'session': '2025/2026'
#         }
#         response = self.client.post(url, data)

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(Register.objects.count(), 0)

#     def test_duplicate_registration_rejected(self):
#         """The same student cannot register for the same course twice in the same session."""
#         url = reverse('register-list')
#         data = {
#             'student': self.student_100.id,
#             'course': self.course_100.id,
#             'session': '2025/2026'
#         }

#         # First registration should succeed
#         first_response = self.client.post(url, data)
#         self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)

#         # Second identical registration should be rejected
#         second_response = self.client.post(url, data)
#         self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(Register.objects.count(), 1)
        
#     def test_course_department_accepted(self):
#         """A student can register for a course for his/her department"""
#         url = reverse ('register-list')
#         data = {
#             'student': self.student_300.id,
#             'course': self.course_300.id,
#             'department': self.department.id,
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Register.objects.count(), 1)
        
#     def test_course_department_mismatch_rejected(self):
#         """A student cannot register for a course that is not for his/her department"""
#         url = reverse ('register-list')
#         data = {
#             'student': self.student_300.id,
#             'course': self.course_300_1.id,
#             'department': self.department_1.id,
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(Register.objects.count(), 0)
        
#     def test_six_courses(self):
#         url = reverse ('register-list')
#         for i in range(6):
#             c = Course.objects.create(
#                 department=self.department,
#                 course_code=f'CSC101{i}',
#                 course_title=f'Intro to Programming{i}',
#                 level=100,
#                 semester='first',
#                 course_unit=3
#             )
#             data = {
#                 'student': self.student_300.id,
#                 'course': c.id,
#                 'session': '2025/2026'
#             }
#             response = self.client.post(url, data)
#             self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
#         seventh = Course.objects.create(
#             department=self.department,
#             course_code='CSC107',
#             course_title='Intro to Programming 7',
#             level=100,
#             semester='first',
#             course_unit=3
#         )
#         data = {
#             'student': self.student_300.id,
#             'course': seventh.id,
#             'session': '2025/2026'
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(Register.objects.count(), 6)