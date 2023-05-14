"""Сериализаторы для моделей."""

import datetime as dt
import re

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from reviews.models import Category, Comment, Genre, Review, Title, User

MAX_USERNAME_LEN = 150
MAX_EMAIL_LEN = 50
MAX_CONFIRMCOD_LEN = 50


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=MAX_EMAIL_LEN)
    username = serializers.CharField(max_length=MAX_USERNAME_LEN)

    class Meta:
        fields = ('email', 'username')
        model = User

    def validate(self, data):
        data = super().validate(data)
        pattern = r'^[\w.@+-]+$'
        email = data.get('email')
        username = data.get('username')
        if (not User.objects.filter(email=email, username=username).exists()
            and any((User.objects.filter(email=email).exists(),
                     User.objects.filter(username=username).exists()))):
            raise serializers.ValidationError('Это имя или почта заняты.')

        if not re.match(pattern, username) or username == 'me':
            raise serializers.ValidationError('Неверный формат username')

        return data


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=MAX_USERNAME_LEN)
    confirmation_code = serializers.CharField(max_length=MAX_CONFIRMCOD_LEN)

    class Meta:
        fields = ('username', 'confirmation_code')
        model = User

    def validate(self, data):
        data = super().validate(data)
        user = get_object_or_404(User, username=data['username'])
        if user.confirmation_code != data['confirmation_code']:
            raise serializers.ValidationError('Неверный код.')

        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug')

    class Meta:
        fields = ('__all__')
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField()

    class Meta:
        fields = ('__all__')
        model = Title
        read_only_fields = ('genre', 'category', 'rating')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def create(self, validated_data):
        title = validated_data['title']
        author = validated_data['author']
        if Review.objects.filter(title=title, author=author).exists():
            raise ValidationError('Отзыв можно оставлять только один раз.')
        review = Review.objects.create(**validated_data)
        return review


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
