import logging

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from logics.models import URLMapping
from logics.serializers import RegistrationSerializer
from logics.utils import store_url_to_db


@api_view(['GET', 'POST'])
@permission_classes([])
def registration_view(request):
    """
    this function is used for registering a user into the system.
    :param request:
    :return:
    """
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.get(user=user).key
        response = dict(message='successfully registered.', token=token)
        return Response(response, status=status.HTTP_200_OK)
    else:
        response = serializer.errors
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([])
def login_view(request):
    """
    this function is used for returning an auth token to a valid user.
    :param request:
    :return:
    """
    try:
        user = User.objects.get(username=request.data['username'])
        if user.password != request.data['password']:
            raise Exception
        token, created = Token.objects.get_or_create(user=user)
        response = dict(message='login successful.', token=token.key)
        return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        logging.debug(e)
        return Response({
            'error': 'provided data is incorrect.'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def shorten_url(request):
    """
    this method implements the API logic for shortening the URL.
    :param request:
    :return:
    """
    try:
        url = request.data.get('url')
        if url is None:
            raise Exception
        response = store_url_to_db(url)
        if response['success']:
            return Response({
                'message': "URL shortened and saved into database successfully!",
                'shortened_url': response['message'],
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'message': response['message']
            }, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response({
            'message': 'Please make sure the keys entered are correct.'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_url_from_hash(request):
    """
    this method is used to retrieve the url corresponding to a specific hash.
    :param request:
    :return:
    """
    url_hash = request.data.get('hash')
    try:
        instance = URLMapping.objects.get(url_hash=url_hash)
        return Response({
            'url': instance.url
        }, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({
            'message': "The hashed url entered does not exist in the database."
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({
            'message': "Some error occurred, please try again."
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_hash_from_url(request):
    """
    this method is used to retrieve the hash for a specific url.
    :param request:
    :return:
    """
    url = request.data.get('url')
    try:
        instance = URLMapping.objects.get(url=url)
        return Response({
            'url': instance.url_hash
        }, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({
            'message': "The entered url does not exist in the database."
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({
            'message': "Some error occurred, please try again."
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
