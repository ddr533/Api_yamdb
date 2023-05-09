"""Сериализаторы для моделей."""

from rest_framework import serializers
from reviews.models import Comment, Review


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
