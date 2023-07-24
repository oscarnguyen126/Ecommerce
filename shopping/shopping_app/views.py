from .models import Cart, Item, Category
from .serializers import CartSerializer, ItemSerializer, ItemListSerializer, CategorySerializer, CategoryListSerializer
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser



class ItemList(APIView):
    def get(self, request):
        item = Item.objects.all()
        return JsonResponse(ItemListSerializer(item, many=True).data, status=200, safe=False)


    def post(self, request):
        data = JSONParser().parse(request)
        serializer = ItemSerializer(data=data)

        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        item = serializer.save()
        item.save()
        return JsonResponse(serializer.data, status=201, safe=False)


class ItemDetails(APIView):
    def get_item(self, pk):
        return get_object_or_404(Item, pk=pk)


    def get(self, request, pk):
        item = self.get_item(pk=pk)
        serializer = ItemListSerializer(item)
        return JsonResponse(serializer.data, status=200)


    def put(self, request, pk):
        item = self.get_item(pk=pk)
        data = JSONParser().parse(request)
        serializer = ItemSerializer(data=data)

        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)
        
        serializer.save()
        item.save()
        return JsonResponse(serializer.data, status=200)


    def delete(self, request, pk):
        item = self.get_item(pk=pk)
        item.delete()
        return JsonResponse({"msg": "Item removed"}, status=204)


class CategoryList(APIView):
    def get(self, request):
        category = Category.objects.all()
        serializer = CategoryListSerializer(category, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)


    def post(self, request):
        data = JSONParser().parse(request)
        serializer = CategorySerializer(data=data)

        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        category = serializer.save()
        category.save()
        return JsonResponse(serializer.data, status=200)


class CategoryDetails(APIView):
    def get_category(self, pk):
        return get_object_or_404(Category, pk=pk)


    def get(self, request, pk):
        category = self.get_category(pk=pk)
        serializer = CategoryListSerializer(category)
        return JsonResponse(serializer.data, status=200)


    def put(self, request, pk):
        category = self.get_category(pk=pk)
        data = JSONParser().parse(request)
        serializer = CategorySerializer(category, data=data)

        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        category = serializer.save()
        category.save()
        return JsonResponse(serializer.data, status=200)


    def delete(self, request, pk):
        category = self.get_category(pk=pk)
        category.delete()
        return JsonResponse({"msg": "Category removed"}, status=204)
