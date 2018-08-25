import base64
import json

from Crypto.Cipher import AES

from books.models import Books

cipher = AES.new("TheBestSecretKey")
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[:-ord(s[len(s)-1:])]


def decrypt(encoded):
    return unpad(cipher.decrypt(base64.urlsafe_b64decode(encoded)))


def encrypt(text):
    return base64.urlsafe_b64encode(cipher.encrypt(pad(text)))


REQUIRED_PARAMS_BOOKS = ['name', 'type', 'isbn', 'description', 'author_name', 'signed', 'price']
REQUIRED_PARAMS_LOGIN = ['username', 'password']


def is_exist_in_db(isbn_id=None):
    if Books.objects.filter(isbn=isbn_id).count():
        return True
    else:
        return False


def is_valid_id(request_id):
    try:
        int(request_id)
        return True
    except ValueError, e:
        return False


def is_valid_json(req_json):
    try:
        rjson = json.loads(req_json)
    except:
        rjson = req_json
    if not type(rjson) == dict:
        return False, "The provided JSON {} is not valid.".format(req_json)
    else:
        return True, rjson


def is_having_required_params(requested_json, required_properties):
    if sorted(requested_json.keys()) == sorted(required_properties):
        return True, requested_json
    else:
        missing = ' , '.join([str(i) for i in set(required_properties)-set(requested_json)])
        return False, "The provided JSON is missing required parameters. Your body has missed {} properties.".format(missing)


def is_valid_properties(requested_json):
    for item in requested_json.keys():
        if item not in REQUIRED_PARAMS_BOOKS:
            return False
    return True

