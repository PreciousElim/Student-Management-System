from rest_framework import serializers
from .models import Register

class RegisterSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    course_title = serializers.SerializerMethodField()
    
    class Meta:
        model = Register
        fields = ['student', 'course', 'session', 'registered_date','student_name', 'course_title']
        
        
    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"    
    
    def get_course_title(self, obj):
        return f"{obj.course.course_code} - {obj.course.course_title}" 
    
        
    def validate(self, attrs):
        if attrs['student'].level < attrs['course'].level:
            raise serializers.ValidationError({
                'message':'Course level is above Student level'
            })
        
        if attrs['student'].department != attrs['course'].department:
            raise serializers.ValidationError({
                'message':'Student department and Course department does not match'
            })
        
            
        course_count = Register.objects.filter(
            student = attrs['student'],
            session =attrs ['session']
        ).count()
        if course_count >= 6:
            raise serializers.ValidationError({
                'message' : 'Only six courses can be registered'
            })
        return attrs