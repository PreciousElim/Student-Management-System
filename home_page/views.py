from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Student Management System is Live!")
# Create your views here.
