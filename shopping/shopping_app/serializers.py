from rest_framework import serializers
from .models import Cart, Category, Item


class CartSerializer(serializers.ModelSerializer):
    items = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name')

    class Meta:
        model = Cart
        fields = ['id', 'status', 'items']

    def create(self, validated_data):
        return Cart(**validated_data)


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'quantity']

    def create(self, validated_data):
        return Item(**validated_data)


class ItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'price', 'quantity']


class CategorySerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = ['name', 'item']

    def create(self, validated_data):
        return Category(**validated_data)


    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        return  instance


class CategoryListSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'item']
