from django.urls import path
from .views import StudentList, StudentDetail

urlpatterns = [
    path('sms/', StudentList.as_view(), name ='StudentList'),
    path('sms/<int:pk>/', StudentDetail.as_view(), name ='StudentDetail'),
]