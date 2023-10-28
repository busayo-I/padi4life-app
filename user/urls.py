from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.user_sign_up, name='create padi4life account'),
    path('login/', views.user_login, name='login')
]