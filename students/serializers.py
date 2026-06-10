from rest_framework import serializers
from .models import Student
from courses.models import Course
from courses.serializers import CourseSerializer


class StudentSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            'id',
            'first_name',
            'last_name',
            'matric_number',
            'email',
            'department',
            'level',
            'age',
            'courses'
        ]

    def get_courses(self, obj):
        courses = Course.objects.filter(
            department=obj.department,
            level=obj.level
        )
        return CourseSerializer(courses, many=True).data