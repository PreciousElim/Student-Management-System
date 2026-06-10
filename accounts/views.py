from django.shortcuts import render
from .models import User
from .serializers import AccountSerializer
from rest_framework import generics, permissions, status
from rest_framework.response import Response


class CreateAccount (generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer
    # permission_classes = [permissions.IsAdminUser]
    permission_classes = [permissions.AllowAny]
    
    def create (self,request, *args, **kwargs):
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        
        return Response ({
            'message': 'Account created successfully'},
            status = status.HTTP_201_CREATED
        )
    
# Create your views here.