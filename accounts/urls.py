from django.urls import path
from.views import CreateAccount

urlpatterns = [
    path('register/', CreateAccount.as_view(), name='Creating Account'),
]