
from rest_framework import serializers
from .models import PadicoinAccount

class PadicoinAccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PadicoinAccount
        fields = ('balance', 'pin')

class PadicoinAccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PadicoinAccount
        fields = ('account_id', 'balance', 'earned_today', 'last_activity_date')
