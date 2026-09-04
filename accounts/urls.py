from django.urls import path
from.views import CreateAccount, LogoutView

urlpatterns = [
    path('register/', CreateAccount.as_view(), name='Creating Account'),
    path('logout/', LogoutView.as_view(), name='log-out'),
]