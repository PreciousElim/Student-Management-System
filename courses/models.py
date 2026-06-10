from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course_code = models.CharField(max_length=10)
    course_title = models.CharField(max_length=100)
    level = models.IntegerField(choices=[(100, "100 Level"), (200, "200 Level"), (300, "300 Level"), (400, "400 Level")])
    semester = models.CharField(max_length=20, choices=[("first", "First Semester"), ("second", "Second Semester")])
    course_unit = models.IntegerField()

    def __str__(self):
        return f'{self.course_code} - {self.course_title}'