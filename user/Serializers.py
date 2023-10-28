from rest_framework import serializers
from .models import Users

class UserSerializer(serializers.ModelSerializer):
    class mata:
        model = Users
        fileds = '__all__'


class UserLoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField(write_only=True)