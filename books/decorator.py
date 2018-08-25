from functools import wraps
from rest_framework.response  import Response
from django.contrib.auth.models import User

from Crypto.Cipher import AES
import base64
cipher = AES.new("TheBestSecretKey")
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[:-ord(s[len(s)-1:])]

def decrypt(encoded):
    try:
        return unpad(cipher.decrypt(base64.urlsafe_b64decode(encoded)))
    except:
        return False


def is_exist_in_db(user_id):
    if User.objects.filter(id=user_id):
        return True, User.objects.filter(id=user_id)[0]
    else:
        return False, ""


def login_required(f):
    @wraps(f)
    def wrap(self, request, *args, **kwargs):
        validation_token = request.META.get('HTTP_AUTHORIZATION')


        if not validation_token:
            return Response({"error": True, "message": "There is no header. Please send authorized header key-value pairs"}, status=500)
        user_id = decrypt(validation_token)
        if not user_id:
            return Response({"error": True, "message": "Unable to decrypt the value. Please check the encoded value again."}, status=500)
        is_exist, user = is_exist_in_db(user_id)
        if not is_exist:
            return Response({"error": True, "message": "The provided user_id in header is not exist in DB. Pleaase check value again"}, status=500)
        return f(self, request, *args, **kwargs)
    return wrap
