from django.urls import path
from .views import RegisterList, RegisterDetailsView


urlpatterns = [
    path('register/', RegisterList.as_view(), name='register-list'),
    path('register/<int:pk>/', RegisterDetailsView.as_view(), name='register-details'),
]