from rest_framework import serializers
from .models import Car, Comment
from django.contrib.auth.models import User

# Сериализатор для модели автомобиля
class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'year', 'description', 'created_at', 'updated_at', 'owner']


# Сериализатор для модели комментария
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'author', 'car']

        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

