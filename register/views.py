from django.shortcuts import render
from .serializers import RegisterSerializer
from .models import Register
from rest_framework import generics, permissions


class RegisterList(generics.ListCreateAPIView):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
    
class RegisterDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
# Create your views here.
