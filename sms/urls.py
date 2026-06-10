"""
URL configuration for sms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from home_page.views import home

urlpatterns = [
    #for apps
    path('', include('home_page.urls')),
    
    path('admin/', admin.site.urls),
    path('api/accounts/', include("accounts.urls")),
    path('api/students/', include("students.urls")),
    path('api/courses/', include('courses.urls')),
    path('api/register/', include('register.urls')),
    #for jwt authentication
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]
    




