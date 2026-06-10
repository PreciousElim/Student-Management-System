from django.urls import path
from .views import DepartmentList, DepartmentDetail, CourseList, CourseDetail


urlpatterns = [
    path('departments/', DepartmentList.as_view(), name='department-list'),
    path('departments/<int:pk>/', DepartmentDetail.as_view(), name='department-detail'),
    path('course/', CourseList.as_view(), name='course-list'),
    path('course/<int:pk>/', CourseDetail.as_view(), name='course-detail')
]