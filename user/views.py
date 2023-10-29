from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Users
from .Serializers import UserSerializer, UserLoginSerializer, UserUpdateSerializer, UserDetailSerializer
from django.contrib.auth.hashers import make_password, check_password
from django.utils.text import slugify
import logging

@api_view(['POST'])
@permission_classes([AllowAny])
def user_sign_up(request):
    try:
        if request.method == 'POST':
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            email = request.data.get('email')
            username = request.data.get('username')
            password = request.data.get('password')
            address = request.data.get('address')

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
            new_user = Users(first_name=first_name, last_name=last_name, email=email, username=username, password=hashed_password, address=address, slug=slug)
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
    
@api_view(['PUT'])
def update_user_details(request, slug):
    try:
        user = Users.objects.get(slug=slug)

        # Check if the user exists
        if user is None:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'PUT':
            serializer = UserUpdateSerializer(user, data=request.data)

            if serializer.is_valid():
                serializer.save()
                
                updated_user = Users.objects.get(slug=slug)
                serializer_user = UserUpdateSerializer(updated_user)
                massage = {
                    'message': 'User details updated successfully',
                    'details': serializer_user.data
                }    
                return Response(massage, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Users.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        error_message = str(e)
        response = {
            'status_message': 'error',
            'message': 'An error occurred: ' + error_message,
        }
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def get_user_details(request, slug):
    try:
        user = Users.objects.get(slug=slug)

        if user is not None:
            serializer = UserDetailSerializer(user)  # Create a serializer for user details

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    except Users.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        error_message = str(e)
        response = {
            'status_message': 'error',
            'message': 'An error occurred: ' + error_message,
        }
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)