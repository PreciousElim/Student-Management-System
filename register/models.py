from django.db import models
from students.models import Student
from courses.models import Course

class Register(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name = 'registration')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name = 'registration')
    session = models.CharField(max_length=9, default='2025/2026')
    registered_date = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering =["-registered_date"]
        unique_together = ['student', 'course', 'session']
        
        
    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} registered {self.course.course_title} {self.course.course_code}"
# Create your models here.