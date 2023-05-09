"""Конфигурация маршрутов api."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, ReviewViewSet

app_name = 'api'

router = DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviwes')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<reviwe_id>\d+)/comments',
    CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/', include(router.urls)),
]
