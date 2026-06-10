from django.db import models
from courses.models import Department


class Student(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    matric_number = models.CharField(max_length = 7, unique=True)
    email = models.EmailField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)    
    level = models.IntegerField(choices=[(100, "100 Level"), (200, "200 Level"), (300, "300 Level"), (400, "400 Level")])
    age = models.IntegerField()
    
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {str(self.matric_number)}"
    