from .models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'staff_id',
            'password',
            'confirm_password'
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."}
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')

        user = User.objects.create_user(
            username=validated_data['username'],
            staff_id=validated_data.get('staff_id'),
            password=validated_data['password']
        )

        return user