from django.contrib.auth import authenticate
from drf_yasg import openapi
from rest_framework import serializers
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'mobile_number']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['id']
        swagger_schema_fields = {"required": ['email', 'password'], "type": openapi.TYPE_OBJECT,
                                 "properties": {
                                     "email": openapi.Schema(
                                         title="email",
                                         type=openapi.TYPE_STRING,
                                     ),
                                     "password": openapi.Schema(
                                         title="password",
                                         type=openapi.TYPE_STRING,
                                     ),
                                     "first_name": openapi.Schema(
                                         title="first_name",
                                         type=openapi.TYPE_STRING,
                                     ),
                                     "mobile_number": openapi.Schema(
                                         title="mobile_number",
                                         type=openapi.TYPE_STRING,
                                     ),
                                 }}


class LoginSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.CharField(max_length=100, write_only=True)
    password = serializers.CharField(max_length=100, write_only=True)

    def create(self, validated_data):
        user = authenticate(**validated_data)
        if not user:
            raise Exception('Invalid credentials')
        return user
