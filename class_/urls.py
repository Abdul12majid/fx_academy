from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('contact', views.contact, name='contact'),
    path('classes', views.classes, name='classes'),
    path('login', views.login_user, name='login'),
    path('register', views.register, name='register'),
]