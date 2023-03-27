import logging
from rest_framework.response import Response
from fundoonote import settings
from rest_framework.authentication import SessionAuthentication

import jwt

logging.basicConfig(filename="utils.log",
                    filemode='a',
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class SessionAuth(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class JWT:
    """
    Class for JWT
    """

    def encode(self, data):
        try:
            if not isinstance(data, dict):
                return Response({"message": "Data should be a dictionary"})
            if 'exp' not in data.keys():
                data.update({'exp': settings.JWT_EXP})
            return jwt.encode(data, 'secret', algorithm='HS256')
        except Exception as e:
            logging.error(e)

    def decode(self, token):
        try:
            return jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.exceptions.ExpiredSignatureError:
            return Response({"message": "Token Expired"})
        except jwt.exceptions.InvalidTokenError:
            return Response({"message": "Invalid Token"})
        except Exception as e:
            logging.error(e)


def verify_token(function):
    def wrapper(self, request, *args, **kwargs):

        token = request.headers.get("Token")
        if not token:
            return Response({"message": "token not found"}, status=400)
        decoded = JWT().decode(token)
        if not decoded:
            return Response({"message": "token authentication required"})
        user_id = decoded.get("user_id")
        if not user_id:
            return Response({"message": "Invalid user"}, status=400)
        request.data.update({"user": user_id})
        return function(self, request, *args, **kwargs)

    return wrapper

