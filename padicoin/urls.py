from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>/create-padicoin/', views.create_padicoin_account, name='create_wallet'),
    path('<slug:slug>/padicoin-detail/', views.get_padicoin_account_details, name='wallet_details')
]