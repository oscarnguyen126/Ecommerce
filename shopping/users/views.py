from .models import User
from .serializers import UserSerializer, UserListSerializer, UserUpdateSerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
import json
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from shopping_app.serializers import CartSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import JSONParser



class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        return JsonResponse(UserListSerializer(users, many=True).data, safe=False, status=200)


    def post(self, request):
        user = User.objects.filter(email=request.data['email'])
        if len(user):
            return JsonResponse({"msg":"This email address is already in use"}, status=400)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.save()
            return JsonResponse(serializer.data, status=201, safe=False)


class UserDetails(APIView):
    def get_user(self, pk):
        return get_object_or_404(User, pk=pk)


    def get(self, request, pk):
        user = self.get_user(pk=pk)
        serializer = UserListSerializer(user)
        return JsonResponse(serializer.data)

    def put(self, request, pk):
        user = self.get_user(pk=pk)
        serializer = UserUpdateSerializer(user, data=request.data)

        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)
        
        serializer.save()
        return JsonResponse(serializer.data, status=200)

    def delete(self, request, pk):
        user = self.get_user(pk=pk)
        user.delete()
        return JsonResponse({"msg": "User deleted successfully"}, status=204)


@csrf_exempt
def get_user_cart(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({"msg":"You're not log in"}, status=404)

    user = User.objects.get(pk=pk)
    if request.method == 'GET':
        try:
            cart = user.cart
            serializer = CartSerializer(cart)
            return  JsonResponse(serializer.data, safe=False, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"msg": "Empty cart"}, status=404)

    elif request.method == 'POST':
        current_user = request.user
        data = JSONParser().parse(request)
        serializer = CartSerializer(data=data)

        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        cart = serializer.save()
        cart.user = current_user
        cart.save()
        return JsonResponse(serializer.data, status=201, safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        cart = user.cart
        serializer = CartSerializer(cart, data=data)
        if serializer.is_valid():
            cart = serializer.save()
            cart.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        try:
            cart = user.cart
            cart.delete()
            return JsonResponse({"msg": "All items removed"}, status=204)
        except ObjectDoesNotExist:
            return JsonResponse({"msg": "Empty cart"}, status=404)


@csrf_exempt
def login_view(request):
    data = json.loads(request.body)

    email  = data["email"]
    password = data["password"]

    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse(json.dumps({"current_user": user.id}))
    else:
        return JsonResponse({"msg": "Invalid email or password"})


@csrf_exempt
def logout_view(request):
    logout(request)
    return HttpResponse(json.dumps({"msg": "User Logout successfully"}))
