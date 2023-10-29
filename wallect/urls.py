from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>/wallet-create/', views.create_wallet, name='create_wallet'),
    path('<slug:slug>/wallet-detail/', views.wallet_details, name='wallet_details')
]