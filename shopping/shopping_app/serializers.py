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


    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.description = validated_data['description']
        instance.price = validated_data['price']
        instance.quantity = validated_data['quantity']
        return  instance


class ItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'price', 'quantity', 'categories']


class CategorySerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['name', 'items']

    def create(self, validated_data):
        return Category(**validated_data)


    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        return  instance
    
    def get_items(self, instance):
        items = instance.item_set.all()
        return ItemSerializer(items, many=True).data


class CategoryListSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'items']
        
    def get_items(self, instance):
        items = instance.item_set.all()
        return ItemSerializer(items, many=True).data
