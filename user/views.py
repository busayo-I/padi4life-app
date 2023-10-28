from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Users
from .Serializers import UserSerializer, UserLoginSerializer
from django.contrib.auth.hashers import make_password, check_password
from django.utils.text import slugify
import logging

@api_view(['POST'])
@permission_classes([AllowAny])
def user_sign_up(request):
    try:
        if request.method == 'POST':
            email = request.data.get('email')
            password = request.data.get('password')
            username = request.data.get('username')

            if not email or not password or not username:
                error = {'error': 'Email, password, and username are required.'}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

            if Users.objects.filter(email=email).exists():
                error = {'error': 'Email already exists.'}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

            if Users.objects.filter(username=username).exists():
                error = {'error': 'Username already exists.'}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

            # Generate a unique slug based on the username
            slug = slugify(username)
            count = 1
            while Users.objects.filter(slug=slug).exists():
                # If a user with the same slug exists, append a count to make it unique
                slug = f"{slug}-{count}"
                count += 1

            # Hash the password
            hashed_password = make_password(password)

            # Create the user with a unique slug
            new_user = Users(email=email, password=hashed_password, username=username, slug=slug)
            new_user.save()

            data = {
                'message': "Padi4life account created successfully",
                'Email': email,
                'Username': username,
            }
            return Response(data, status=status.HTTP_201_CREATED)

    except Exception as e:
        error_message = str(e)
        response = {
            'status_message': 'error',
            'message': 'An error occurred: ' + error_message,
        }
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    try:
        if request.method == 'POST':
            email_or_username = request.data.get('email_or_username')
            password = request.data.get('password')

            if not email_or_username or not password:
                error = {'error': 'Both email/username and password are required.'}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

            # Query your custom user model to find the user based on email or username
            try:
                user = Users.objects.get(email=email_or_username)
            except Users.DoesNotExist:
                try:
                    user = Users.objects.get(username=email_or_username)
                except Users.DoesNotExist:
                    user = None

            if user is not None and check_password(password, user.password):
                # Successful login
                data = {
                    'message': 'Login successful',
                    'user_id': user.id,
                    'username': user.username,
                    'slug': user.slug
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                # Invalid login credentials
                error = {'error': 'Invalid login credentials.'}
                return Response(error, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        error_message = str(e)
        response = {
            'status_message': 'error',
            'message': 'An error occurred: ' + error_message,
        }
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)