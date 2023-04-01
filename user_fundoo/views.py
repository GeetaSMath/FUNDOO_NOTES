from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from note.util import JWT
from .models import User
import json
from .tasks import send_mail_func

def user_register(request):
    """
    This method register details and return response wether registation is register or not
    :param request:
    :return:
    """
    try:
        data = json.loads(request.body)
        if request.method == 'POST':
            user = User.objects.create_user(first_name=data.get('first_name'), email=data.get('email'),
                                            password=data.get('password'), mobile_number=data.get('mobile_number'))
            print(user.first_name)
            # send_mail_func.delay(first_name=user.first_name, recipient=user.email)
            send_mail_func(user.first_name, user.email)



            return JsonResponse(
                {'data': {"full_name": user.first_name, "email": user.email, "mobile_number": user.mobile_number},
                 'message': "registration successfully", "status": 201}, status=201)
        return JsonResponse({'data': {}, 'message': "method not allowed", "status": 405}, status=405)

    except Exception as e:
        return JsonResponse({"data": {}, "message": str(e), "status": 400}, status=400)


def user_login(request):
    """
        This method logins registration based on username and password.
        Returns login success or failed...
    """
    try:
        data = json.loads(request.body)
        # data.update({"user":request.user.id})

        if request.method == 'POST':
            user = authenticate(email=data.get('email'), password=data.get('password'))
            login(request,user)
            token = JWT().encode(data={"user_id": user.id})
            if user:
                return JsonResponse({"message": "login succesfully", "token": token, "status": 201}, status=201)
            return JsonResponse({"message": "invalid credentials ", "status": 406}, status=406)
        return JsonResponse({"message": "method not allowed", "status": 405}, status=405)
    except Exception as e:
        return JsonResponse({"data": {}, "message": e.args[0], "status": 400}, status=400)

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