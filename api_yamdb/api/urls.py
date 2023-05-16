"""Конфигурация маршрутов api."""

from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserMeAPI, UserViewSet,
                    signup, token)

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
router.register(r'users', UserViewSet, basename='user')

v1_urls = [
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', token, name='token'),
    path('users/me/', UserMeAPI.as_view(), name='userme')
]

urlpatterns = [
    path('v1/', include(v1_urls)),
    path('v1/', include(router.urls)),
]
