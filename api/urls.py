from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello, name='hello'),
    path('signup/', views.api_signup, name='api_signup'),
    path('login/', views.api_login, name='api_login'),
]
