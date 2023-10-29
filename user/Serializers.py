from rest_framework import serializers
from .models import Users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fileds = '__all__'


class UserLoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'phone_number', 'country', 'address', 'date_of_birth', 'profile_picture')

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'username', 'phone_number', 'country', 'address', 'date_of_birth', 'profile_picture', 'created_at', 'updated_at')