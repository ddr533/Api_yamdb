"""Конфигурация маршрутов api."""

from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenVerifyView

from .views import (CategoryViewSet, GenreViewSet, TitleViewSet,
                    CommentViewSet,
                    ReviewViewSet, UserViewSet, signup, token)


app_name = 'api'

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('v1/auth/signup/', signup,

          name='signup'),
    path('v1/auth/token/', token,
          name='token'),
    path('users/<str:username>/',
         UserViewSet.as_view({'get': 'retrieve'}),
         name='user-detail'),
    path('v1/', include(router.urls)),
]
