from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('contact', views.contact, name='contact'),
    path('classes', views.classes, name='classes'),
    path('login', views.login_user, name='login'),
    path('register', views.register, name='register'),
    path('success/', views.success_view, name='payments-success'),
    path('cancel/', views.cancel_view, name='payments-cancel'),
    path('verify', views.verify, name='verify'),
    path('packages', views.packages, name='packages'),
    path('webhook/', views.coinbase_webhook),
]