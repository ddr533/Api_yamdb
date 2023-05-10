"""Обработчики для сериализаторов."""

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from reviews.models import Review

from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Обработчик запросов к отзывам на произведения."""

    serializer_class = ReviewSerializer
    # permission_classes =

    # def perform_create(self, serializer):
    #     title_id = self.kwargs.get('title_id')
    #     title = get_object_or_404(Title, id=title_id)
    #     serializer.save(author=self.request.user, title_id=title)

    # def get_queryset(self):
    #     title_id = self.kwargs.get('title_id')
    #     title = get_object_or_404(Title, id=title_id)
    #     return title.feedbacks.all()


class CommentViewSet(viewsets.ModelViewSet):
    """Обработчик запросов к комментариям на отзывы."""

    serializer_class = CommentSerializer
    # permission_classes =

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(review_id=review)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()
