from django.contrib.auth.views import LoginView
from django.urls import path

from apps.registration.views import RegistrationView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegistrationView.as_view(), name='register'),
]
