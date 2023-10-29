from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import PadicoinAccount
from user.models import Users
from .serializers import PadicoinAccountCreateSerializer, PadicoinAccountDetailSerializer
from django.utils import timezone

@api_view(['POST'])
def create_padicoin_account(request, slug):
    try:
        user = Users.objects.get(slug=slug)

        if user is not None:
            serializer = PadicoinAccountCreateSerializer(data=request.data)

            if serializer.is_valid():
                # Create the PADICOIN account for the user
                account_data = {
                    'user': user,
                    'balance': serializer.validated_data['balance'],
                    'pin': serializer.validated_data['pin'],
                    'earned_today': 0.0,  # Initialize earned_today to 0.0
                    'last_activity_date': timezone.now(),  # Set the last activity date to the current timestamp
                }
                padicoin_account = PadicoinAccount(**account_data)
                padicoin_account.save()

                # Return account details in the response
                response_data = {
                    'message': 'PADICOIN account created successfully',
                    'account_id': padicoin_account.account_id,
                    'balance': padicoin_account.balance,
                }

                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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


@api_view(['GET'])
def get_padicoin_account_details(request, slug):
    try:
        user = Users.objects.get(slug=slug)

        if user is not None:
            padicoin_account = PadicoinAccount.objects.get(user=user)

            if padicoin_account:
                serializer = PadicoinAccountDetailSerializer(padicoin_account)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'PADICOIN account not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    except Users.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except PadicoinAccount.DoesNotExist:
        return Response({'message': 'PADICOIN account not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        error_message = str(e)
        response = {
            'status_message': 'error',
            'message': 'An error occurred: ' + error_message,
        }
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
