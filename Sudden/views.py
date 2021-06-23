from django.contrib.auth import authenticate
from django.http import JsonResponse
from django_tenants.utils import schema_context
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from customer.serializer import ClientSerializer
from utilities.api_response import APIFailure, APISuccess
from utilities.python_utils import get_schema

from .serializer import UserSerializer


class Login(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        with schema_context(get_schema(request)):
            username = request.data.get("username")
            password = request.data.get("password")
            if username is None or password is None:
                return APIFailure(
                    'Please provide both username and password',
                    HTTP_400_BAD_REQUEST
                )
            user = authenticate(username=username, password=password)
            if not user:
                return APIFailure(
                    'Invalid Credentials',
                    HTTP_404_NOT_FOUND
                )
            token, _ = Token.objects.get_or_create(user=user)
            json_ = UserSerializer(user).data
            json_['token'] = token.key
            return APISuccess(
                'Login Successful',
                json_,
            )


class Signup(APIView):
    permission_classes = [AllowAny]

    # {
    # REQUEST DATA FORM
    #     username
    #     email
    #     password
    #     client
    #     domain_url,
    #     title: (staff, superuser, None)
    # }

    def post(self, request):
        context = {"schema": get_schema(request), 'title': request.data.get('title', None)}
        serializer = UserSerializer(data=request.data, context=context)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                json_ = serializer.data
                json_['token'] = token.key
            else:
                return APIFailure(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return APIFailure(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return APISuccess('User created successfully', json_, status.HTTP_201_CREATED)


class ClientSignup(APIView):
    permission_classes = [AllowAny]

    # {
    # REQUEST DATA FORM
    #     username
    #     email
    #     password
    #     client
    #     domain_url,
    # }

    def post(self, request):
        json_ = {}
        client_serializer = ClientSerializer(data=request.data, context=request.data.get('domain_url'))
        if client_serializer.is_valid():
            client = client_serializer.save()
            if client:
                json_['client'] = client_serializer.data
            else:
                return APIFailure(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            context = {"schema": client.schema_name, 'title': 'superuser'}
            serializer = UserSerializer(data=request.data, context=context)
            if serializer.is_valid():
                user = serializer.save()
                if user:
                    token, _ = Token.objects.get_or_create(user=user)
                    json_.update(serializer.data)
                    json_['token'] = token.key
                else:
                    return APIFailure(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return APIFailure(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return APISuccess('User created successfully', json_, status.HTTP_201_CREATED)
        else:
            return APIFailure(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def home(request):
    json_ = {'host': request.get_host(), 'schema_name': get_schema(request)}
    return JsonResponse(json_, safe=False)
