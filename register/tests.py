from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from students.models import Student
from courses.models import Course, Department
from .models import Register

User = get_user_model()


class RegisterTests(APITestCase):

    def setUp(self):
        # A logged-in user to make authenticated requests
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        # Shared department for all courses/students
        self.department = Department.objects.create(
            name='Computer Science',
            )

        # A 100 level student
        self.student_100 = Student.objects.create(
            first_name='Ada',
            last_name='Lovelace',
            matric_number='CSC001',
            email='ada@example.com',
            department=self.department,
            level=100,
            age=18
        )

        # A matching 100 level course
        self.course_100 = Course.objects.create(
            department=self.department,
            course_code='CSC101',
            course_title='Intro to Programming',
            level=100,
            semester='first',
            course_unit=3
        )

        # A mismatched 300 level course
        self.course_300 = Course.objects.create(
            department=self.department,
            course_code='CSC301',
            course_title='Advanced Algorithms',
            level=300,
            semester='first',
            course_unit=3
        )

    def test_successful_registration(self):
        """A student can register for a course at their own level."""
        url = reverse('register-list')
        data = {
            'student': self.student_100.id,
            'course': self.course_100.id,
            'session': '2025/2026'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Register.objects.count(), 1)

    def test_level_mismatch_rejected(self):
        """A 100 level student cannot register for a 300 level course."""
        url = reverse('register-list')
        data = {
            'student': self.student_100.id,
            'course': self.course_300.id,
            'session': '2025/2026'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Register.objects.count(), 0)

    def test_duplicate_registration_rejected(self):
        """The same student cannot register for the same course twice in the same session."""
        url = reverse('register-list')
        data = {
            'student': self.student_100.id,
            'course': self.course_100.id,
            'session': '2025/2026'
        }

        # First registration should succeed
        first_response = self.client.post(url, data)
        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)

        # Second identical registration should be rejected
        second_response = self.client.post(url, data)
        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Register.objects.count(), 1)