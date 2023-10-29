from rest_framework import serializers
from .models import Wallet

class WalletCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('balance', 'pin', 'bvn', 'currency')

class WalletDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('wallet_id', 'balance', 'account_number', 'account_name', 'currency', 'created_at', 'updated_at')