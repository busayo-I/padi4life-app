from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.user_sign_up, name='create padi4life account'),
    path('login/', views.user_login, name='login'),
    path('update/<slug:slug>/', views.update_user_details, name='update_user_details'),
    path('details/<slug:slug>/', views.get_user_details, name='get_user_details'),
]