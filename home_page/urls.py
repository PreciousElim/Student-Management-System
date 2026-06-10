from django.urls import path
from accounts.views import CreateAccount
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', CreateAccount.as_view(), name='Creating Account'),
    path('login/', obtain_auth_token, name='Login')
]