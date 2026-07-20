from rest_framework import serializers
from .models import Register

class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Register
        fields = ['student', 'course', 'session', 'registered_date']
        
        
    def validate(self, attrs):
        if attrs['student'].level != attrs['course'].level:
            raise serializers.ValidationError({
                'message' : 'Student level and course level does not match'
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