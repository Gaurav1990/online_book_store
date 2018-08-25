from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from books.models import Books
from books.decorator import login_required
from books import utils, constants


class LoginAPI(APIView):

    @csrf_exempt
    def post(self, request):
        is_valid, request_data = utils.is_valid_json(request.data)
        if not is_valid:
            msg = {
                "error": True,
                "message": request_data
            }
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        is_req_prop_valid, requested_json = utils.is_having_required_params(request_data, utils.REQUIRED_PARAMS_LOGIN)
        if not is_req_prop_valid:
            msg = {
                "error": True,
                "message": requested_json
            }
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=requested_json['username']).exists():
            user = User.objects.get(username=requested_json['username'])
            is_authenticated = authenticate(username=requested_json['username'],password=requested_json['password'])

            if is_authenticated:
                login(request, is_authenticated)
                encoded=utils.encrypt(str(user.id))

                response_data = {
                    "token": encoded,
                    "message": constants.USER_LOGGED_IN
                }
                response=Response(response_data, status=status.HTTP_200_OK)
                response.set_cookie("book_token", encoded)

                return response

            else:
                msg = {
                    "error": True,
                    "message": constants.INVALID_PASSWORD
                }
                return Response(msg,status=status.HTTP_400_BAD_REQUEST)
        else:
            msg = {
                "error": True,
                "message": constants.INVALID_USER
            }
            return Response(msg,status=status.HTTP_400_BAD_REQUEST)


class BookSingleAPIs(APIView):

    @csrf_exempt
    @login_required
    def get(self, request, isbn_id=None):
        is_exist = utils.is_exist_in_db(isbn_id)
        if not is_exist:
            msg = {
                "error": True,
                "message": constants.INVALID_ID
            }
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            book_dict = model_to_dict(Books.objects.get(isbn = isbn_id))
            response = Response(book_dict, status=status.HTTP_200_OK)
            return response

    @csrf_exempt
    @login_required
    def post(self, request):
        is_valid, request_data = utils.is_valid_json(request.data)
        if not is_valid:
            msg = {
                "error": True,
                "message": request_data
            }
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        is_req_prop_valid, required_params=utils.is_having_required_params(request_data, utils.REQUIRED_PARAMS_BOOKS)
        if not is_req_prop_valid:
            msg = {
                "error": True,
                "message": required_params
            }
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        book = Books.objects.create(
            name=required_params["name"],
            type=required_params["type"],
            isbn=required_params["isbn"],
            description=required_params["description"],
            author_name=required_params["author_name"],
            signed=required_params["signed"],
            price=required_params["price"]
        )
        return Response({"book_id": book.pk, "msg": constants.SUCCESS_MSG_NEW_ENTRY}, status=status.HTTP_201_CREATED)

    @csrf_exempt
    @login_required
    def put(self, request, isbn_id=None):
        if not isbn_id:
            msg = {
                "error": True,
                "message": constants.INCOMPLETE_DATA
            }
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        is_exist = utils.is_exist_in_db(isbn_id)
        if not is_exist:
            msg = {
                "error": True,
                "message": constants.INVALID_ID
            }
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        is_valid, request_data = utils.is_valid_json(request.data)
        if not is_valid:
            msg = {
                "error": True,
                "message": request_data
            }
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        is_valid = utils.is_valid_properties(request_data)
        if not is_valid:
            msg = {
                "error": True,
                "message": constants.INVALID_PROPERTIES
            }
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        book = Books.objects.get(isbn=isbn_id)
        for item in request_data:
            exec ("book."+str(item)+" = request_data[item]")
        book.save()

        return Response({"book_id": book.pk, "msg": constants.SUCCESS_MSG_UPDATE_ENTRY}, status=status.HTTP_205_RESET_CONTENT)

    @csrf_exempt
    @login_required
    def delete(self, request, isbn_id=None):
        if not isbn_id:
            msg = {
                "error": True,
                "message": constants.INCOMPLETE_DATA
            }
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        is_exist = utils.is_exist_in_db(isbn_id)
        if not is_exist:
            msg = {
                "error": True,
                "message": constants.INVALID_ID
            }
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        book = Books.objects.get(isbn=isbn_id)
        book_id = book.id
        book.delete()
        return Response({"book_id":book_id , "msg": constants.SUCCESS_MSG_DELETE_ENTRY}, status=status.HTTP_202_ACCEPTED)


class BooksListAPI(APIView):
    @csrf_exempt
    @login_required
    def get(self, request):
        books = Books.objects.all()
        book_list = []
        for instance in books:
            book_list.append(model_to_dict(instance))

        response_data = {
            "Book": book_list
        }
        response = Response(response_data, status=status.HTTP_200_OK)
        return response


class AllAvailableUrls(APIView):
    @csrf_exempt
    @login_required
    def get(self, request):
        msg = {
            "GET /books": "Fetch all available book details of the store",
            "GET /book/<isbn_id>": "Fetch detail of particular book",
            "POST /book": "Added new book to the store",
            "PUT /book/<isbn_id>": "Updated information for the books already added to the store",
            "DELETE /book/<isbn_id>": "Delete the book information available in the store"
        }
        response = Response(msg, status=status.HTTP_200_OK)
        return response
