from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
# Autenticação
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import login
# Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CustomAuthToken(ObtainAuthToken):
    '''
    view para gerenciamento de tokens de autenticação
    '''
    @swagger_auto_schema(
        operation_summary='Obter o token de autenticação',
        operation_description='Retorna o token em caso de sucesso na autenticação ou HTTP 401',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username' : openapi.Schema(type=openapi.TYPE_STRING),
                'password' : openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['username', 'password', ],

        ),
        responses={
            status.HTTP_200_OK: 'Token is returned.',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized request.',
        },
    )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, contrext={'request': request})
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({'token': token.key})
            return Response(status=status.HTTP_401_UNAUTHORIZED)
       



# Create your views here.


