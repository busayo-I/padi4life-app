# user_management/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Wallet
from user.models import Users
from .serializers import WalletCreateSerializer, WalletDetailSerializer

@api_view(['POST'])
def create_wallet(request, slug):
    try:
        user = Users.objects.get(slug=slug)

        if user is not None:
            serializer = WalletCreateSerializer(data=request.data)

            if serializer.is_valid():
                # Create the wallet for the user
                wallet_data = {
                    'user': user,
                    'balance': serializer.validated_data['balance'],
                    'pin': serializer.validated_data['pin'],
                    'bvn': serializer.validated_data.get('bvn', None),  # BVN is optional
                    'currency': "Naira",  # Default to Naira
                }
                wallet = Wallet(**wallet_data)
                wallet.save()

                # Return BVN, wallet ID, and balance in the response
                response_data = {
                    'message': 'Wallet created successfully',
                    'bvn': wallet.bvn,
                    'wallet_id': wallet.wallet_id,
                    'balance': wallet.balance,
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
def wallet_details(request, slug):
    try:
        user = Users.objects.get(slug=slug)

        if user is not None:
            wallet = Wallet.objects.get(user=user)

            if wallet:
                serializer = WalletDetailSerializer(wallet)  # Create a serializer for user details

                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'wallet not found'}, status=status.HTTP_404_NOT_FOUND)

    except Users.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Wallet.DoesNotExist:
        return Response({'error': 'wallet not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        error_message = str(e)
        response = {
            'status_message': 'error',
            'message': 'An error occurred: ' + error_message,
        }
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)