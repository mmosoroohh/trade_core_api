from django.urls import path

from .views import (
    LoginAPIView, 
    RegistrationAPIView,
    UserRetrieveUpdateAPIView
)

urlpatterns = [
    path('users/details/', UserRetrieveUpdateAPIView.as_view(), name="specific_user"),
    path('users/regsister/', RegistrationAPIView.as_view(), name="register"),
    path('users/login/', LoginAPIView.as_view(), name="login"),
]
