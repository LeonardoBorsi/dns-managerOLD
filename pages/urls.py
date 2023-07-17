from django.urls import path
from .views import (home, RegisterPageView, LoginPageView, LogoutPageView)


urlpatterns = [
    path("", home, name="home"),
    path('register/', RegisterPageView.as_view(), name='register'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('logout/', LogoutPageView.as_view(), name='logout'),
]
