"""Сериализаторы для моделей."""

import datetime as dt

from rest_framework import serializers

from reviews.models import Category, Genre, GenreTitle, Title, Comment, Review


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('__all__')
        model = Category
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('__all__')
        model = Genre
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleSerializer(serializers.ModelSerializer):
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

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        category = validated_data['category']
        try:
            Category.objects.get(slug=category)
            title = Title.objects.create(**validated_data)
            for genre in genres:
                current_genre = Genre.objects.get(slug=genre)
                GenreTitle.objects.create(genre=current_genre, title=title)
        except Exception:
            raise Exception('Такой записи в базе пока нет')
        return title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    # author = serializers.SlugRelatedField(slug_field='username',
    #                                       read_only=True)
    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    # author = serializers.SlugRelatedField(slug_field='username',
    #                                       read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review_id',)

