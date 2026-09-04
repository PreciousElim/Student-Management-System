from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from courses.models import Department, Course
from register.models import Register
from students.models import Student
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()
# Create your tests here.


class PermissionsTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username = 'adminuser',
            password = 'admin123',
            staff_id = 'staff001',
        )
        self.staff = User.objects.create_user(
            username = 'staff001',
            password = 'staff123',
        )
        self.department = Department.objects.create(
            name = 'Computer Science'
        )
        self.course = Course.objects.create(
            department=self.department,
            course_code='CSC301',
            course_title='Advanced Algorithms',
            level=300,
            semester='first',
            course_unit=3
        )
        self.student = Student.objects.create(
            first_name='Jon',
            last_name='Doe',
            matric_number='CSC002',
            email='jon@example.com',
            department=self.department,
            level=300,
            age=20
        )
        self.registration = Register.objects.create(
            student = self.student,
            course = self.course,
            session = '2025/2026',
        )
        """For random users""" 
    def test_foreign_user_cannot_get_students(self):
        url = reverse ('StudentList')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_foreign_user_cannot_get_courses(self):
        url = reverse ('course-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_foreign_user_cannot_get_departments(self):
        url = reverse ('department-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)    
    def test_foreign_user_cannot_get_register(self):
        url = reverse ('register-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  
         
    def test_foreign_user_cannot_get_students_details(self):
        url = reverse ('StudentDetail', args = [self.student.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_foreign_user_cannot_get_courses_details(self):
        url = reverse ('course-detail', args = [self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_foreign_user_cannot_get_departments_details(self):
        url = reverse ('department-detail', args = [self.department.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)    
    def test_foreign_user_cannot_get_register(self):
        url = reverse ('register-details', args = [self.registration.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_foreign_user_cannot_put_students_details(self):
        url = reverse ('StudentDetail', args = [self.student.id])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_foreign_user_cannot_put_courses_details(self):
        url = reverse ('course-detail', args = [self.course.id])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_foreign_user_cannot_put_departments_details(self):
        url = reverse ('department-detail', args = [self.department.id])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)    
    def test_foreign_user_cannot_put_register(self):
        url = reverse ('register-details', args = [self.registration.id])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_foreign_user_cannot_post_students(self):
        url = reverse ('StudentList')
        data = {
            'first_name':'Jon',
            'last_name':'Doe',
            'matric_number':'CSC002',
            'email':'jon@example.com',
            'department':self.department,
            'level':300,
            'age':20,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Student.objects.count(), 1)
        
    def test_foreign_user_cannot_post_courses(self):
        url = reverse ('course-list')
        data = {
            'department':self.department,
            'course_code':'CSC301',
            'course_title':'Advanced Algorithms',
            'level':300,
            'semester':'first',
            'course_unit':3
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Course.objects.count(), 1)
        
    def test_foreign_user_cannot_post_departments(self):
        url = reverse ('department-list')
        data = {
            'name':'Computer Science'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  
        self.assertEqual(Department.objects.count(), 1)
          
    def test_foreign_user_cannot_get_register(self):
        url = reverse ('register-list')
        data = {
            'student':self.student,
            'course':self.course,
            'session':'2025/2026',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Register.objects.count(), 1)
        
    def test_foreign_user_create_superuser_account(self):
        url = reverse('Creating Account')
        data = {
            'username':'mee',
            'staff_id':'001',
            'password':'1234',
            'confirm_password':'1234'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(User.objects.count(), 2)
   
    def test_foreign_user_create_account(self):
        url = reverse('Creating Account')
        data = {
            'username':'mee',
            'password':'1234',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(User.objects.count(), 2)     
       
        """For authnticated staff's"""
    def test_staff_get_students(self):
        self.client.force_authenticate(user=self.staff)
        url = reverse ('StudentList')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_staff_get_courses(self):
        self.client.force_authenticate(user=self.staff)
        url = reverse ('course-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_staff_get_departments(self):
        self.client.force_authenticate(user=self.staff)
        url = reverse ('department-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)    
    def test_staff_get_register(self):
        self.client.force_authenticate(user=self.staff)
        url = reverse ('register-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        
    def test_staff_get_students_details(self):
        self.client.force_authenticate(user=self.staff)
        url = reverse ('StudentDetail', args = [self.student.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_staff_get_courses_details(self):
        self.client.force_authenticate(user=self.staff)
        url = reverse ('course-detail', args = [self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_staff_get_departments_details(self):
        self.client.force_authenticate(user=self.staff)
        url = reverse ('department-detail', args = [self.department.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)    
    def test_staff_get_register(self):
        self.client.force_authenticate(user=self.staff)
        url = reverse ('register-details', args = [self.registration.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_staff_cannot_put_students_details(self):
        self.client.force_authenticate(user=self.staff)
        url = reverse ('StudentDetail', args = [self.student.id])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def test_staff_cannot_put_courses_details(self):
        self.client.force_authenticate(user=self.staff)
        url = reverse ('course-detail', args = [self.course.id])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def test_staff_cannot_put_departments_details(self):
        self.client.force_authenticate(user=self.staff)
        url = reverse ('department-detail', args = [self.department.id])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)    
    def test_staff_can_put_register(self):
        self.client.force_authenticate(user=self.staff)
        url = reverse ('register-details', args=[self.registration.id])
        data={
            'student': self.student.id,
            'course' : self.course.id,
            'session' : '2025/2029',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_staff_cannot_post_students(self):
        self.client.force_authenticate(user=self.staff)
        url = reverse ('StudentList')
        data = {
            'first_name':'Jon',
            'last_name':'Doe',
            'matric_number':'CSC002',
            'email':'jon@example.com',
            'department':self.department,
            'level':300,
            'age':20,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Student.objects.count(), 1)
            
    def test_staff_cannot_post_courses(self):
        self.client.force_authenticate(user=self.staff)
        url = reverse ('course-list')
        data = {
            'department':self.department,
            'course_code':'CSC301',
            'course_title':'Advanced Algorithms',
            'level':300,
            'semester':'first',
            'course_unit':3
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Course.objects.count(),1)
        
    def test_staff_cannot_post_departments(self):
         self.client.force_authenticate(user=self.staff)
         url = reverse ('department-list')
         data = {
             'name':'Computer Science'
         }
         response = self.client.post(url, data)
         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  
         self.assertEqual(Department.objects.count(), 1)
         
    def test_staff_can_post_register(self):
        self.client.force_authenticate(user=self.staff)
        url = reverse ('register-list')
        data = {
            'student':self.student.id,
            'course':self.course.id,
            'session': '2015/1018',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Register.objects.count(), 2)
        
    def test_staff_cannot_create_superuser_account(self):
        self.client.force_authenticate(user=self.staff)
        url = reverse('Creating Account')
        data = {
            'username':'mee',
            'staff_id':'001',
            'password':'1234',
            'confirm_password':'1234'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.count(), 2)
   
    def test_staff_cannot_create_account(self):
        self.client.force_authenticate(user=self.staff)
        url = reverse('Creating Account')
        data = {
            'username':'mee',
            'password':'1234',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.count(), 2)
    
    def test_staff_can_logout(self):
        self.client.force_authenticate(user=self.staff)
        refresh = RefreshToken.for_user(self.staff)
        url = reverse ('log-out')
        response = self.client.post(url, {'refresh': str(refresh)})
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        # trying to use that same token again
        refresh_url = reverse('refresh-token')
        response = self.client.post(refresh_url, {'refresh': str(refresh)})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_admin_get_students(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse ('StudentList')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_admin_get_courses(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse ('course-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_admin_get_departments(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse ('department-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)    
    def test_admin_get_register(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse ('register-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        
    def test_admin_get_students_details(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse ('StudentDetail', args = [self.student.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_admin_get_courses_details(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse ('course-detail', args = [self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_admin_get_departments_details(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse ('department-detail', args = [self.department.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)    
    def test_admin_get_register(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse ('register-details', args = [self.registration.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_admin_can_put_students_details(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse ('StudentDetail', args = [self.student.id])
        data = {
            'first_name':'John',
            'last_name':'Dooe',
            'matric_number':'CSC004',
            'email':'john@example.com',
            'department':self.department.id,
            'level':300,
            'age':22
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_admin_can_put_courses_details(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse ('course-detail', args = [self.course.id])
        data = {
            'department':self.department.id,
            'course_code':'CSC301.1',
            'course_title':'Advanced Algorithms.1',
            'level':100,
            'semester':'second',
            'course_unit':34
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_admin_can_put_departments_details(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse ('department-detail', args = [self.department.id])
        data = {
            "name": 'Cyber Security'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)    
    def test_admin_can_put_register(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse ('register-details', args=[self.registration.id])
        data={
            'student': self.student.id,
            'course' : self.course.id,
            'session' : '2025/2029',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_post_students(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse ('StudentList')
        data = {
            'first_name':'Jonfy',
            'last_name':'Doeyyh',
            'matric_number':'CSC0028',
            'email':'jonfy@example.com',
            'department':self.department.id,
            'level':300,
            'age':209,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 2)
            
    def test_admin_can_post_courses(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse ('course-list')
        data = {
            'department':self.department.id,
            'course_code':'CSC301111',
            'course_title':'Advanced Algorithms 111',
            'level':400,
            'semester':'first',
            'course_unit':36
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)
        
    def test_admin_can_post_departments(self):
         self.client.force_authenticate(user=self.admin)
         url = reverse ('department-list')
         data = {
             'name':'Computer Science111'
         }
         response = self.client.post(url, data)
         self.assertEqual(response.status_code, status.HTTP_201_CREATED)  
         self.assertEqual(Department.objects.count(), 2)
         
    def test_admin_can_post_register(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse ('register-list')
        data = {
            'student':self.student.id,
            'course':self.course.id,
            'session': '2035/1018',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Register.objects.count(), 2)
        
    def test_admin_can_create_superuser_account(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('Creating Account')
        data = {
            'username':'olu',
            'staff_id':'0011',
            'password':'testing12324',
            'confirm_password':'testing12324'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
   
    def test_admin_can_create_account(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('Creating Account')
        data = {
            'username':'ola',
            'password':'test12324',
            'staff_id':'staff12345',
            'confirm_password':'test12324'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        
    def test_admin_can_logout(self):
        self.client.force_authenticate(user=self.admin)
        refresh = RefreshToken.for_user(self.admin)
        url = reverse ('log-out')
        response = self.client.post(url, {'refresh': str(refresh)})
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        # trying to use that same token again
        refresh_url = reverse('refresh-token')
        response = self.client.post(refresh_url, {'refresh': str(refresh)})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)