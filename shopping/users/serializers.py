from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'role']

    def create(self, validated_data):
        return User(**validated_data)

class UserListSerializer(serializers.ModelSerializer):
    cart = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='description'
     )

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'password',
            'cart',
            'role'
        ]



class UserUpdateSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(
        max_length=255, min_length=6, write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = User
        fields = [
            'email',
            'new_password',
            'role',
        ]

    def update(self, instance, validated_data):
        if validated_data.get("new_password"):
            instance.password = make_password(validated_data["new_password"])
        instance.email = validated_data["email"]
        instance.role = validated_data["role"]
        instance.save()
        return instance