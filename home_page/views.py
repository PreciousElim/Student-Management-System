from django.shortcuts import render



def home(request):
    return render(request, 'home_page/index.html')
# Create your views here.
