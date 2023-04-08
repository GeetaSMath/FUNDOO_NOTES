from drf_yasg.utils import swagger_auto_schema
from .models import User
from .serializers import RegistrationSerializer, LoginSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .tasks import send_mail_func
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import json
from note.util import JWT
from user_fundoo.models import User
from rest_framework.views import Response


class UserRegistration(APIView):
    """Class to register the user"""

    @swagger_auto_schema(request_body=RegistrationSerializer, responses={201: 'Created', 400: 'BAD REQUEST'})
    def post(self, request):
        """Method to register the user"""
        try:
            serializer = RegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            first_name = serializer.data.get("first_name")
            email = serializer.data.get("email")
            send_mail_func(first_name, email)
            # return JsonResponse(message='Registration successful, check email for verification', status=201)
            return Response({"data": serializer.data, "message": 'Registration successful', "status": 201}, status=201)
        except Exception as e:
            return Response({"data": {}, "message": str(e), "status": 400}, status=400)


class UserLogin(APIView):
    """Class to login the user"""

    @swagger_auto_schema(request_body=LoginSerializer, responses={202: 'Login Successful', 400: 'BAD REQUEST'})
    def post(self, request):
        """Method to login the user"""
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            token = JWT().encode({"user_id": serializer.data.get("id")})
            return Response({"data": token, "message": 'Login Successful', "status": 201}, status=201)
        except Exception as e:
            return Response({"data": {}, "message": str(e), "status": 400}, status=400)


def verify_token(request, token=None):
    try:
        decoded = JWT().decode(token)
        user = User.objects.get(email=decoded.get("email"))
        if not user:
            raise Exception("Invalid user")
        user.is_verified = True
        # user.save()
        return JsonResponse({"data": {}, "message": "token verified ", "status": 200}, status=200)
    except Exception as e:
        return JsonResponse({"data": {}, "message": str(e), "status": 400}, status=400)
