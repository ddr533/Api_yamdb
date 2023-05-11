"""Обработчики для представлений."""

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, status
from reviews.models import Category, Genre, Title, Review, User
from .pagination import DefaultPagination
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer,
                          CommentSerializer, ReviewSerializer, UserSerializer,
                          SignUpSerializer, TokenSerializer)
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.utils.crypto import get_random_string
from api_yamdb.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from .permissions import CastomAdminSuperUser, UserUpdateRole


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']

        if username == 'me':
            raise AssertionError()
        
        confirmation_code = get_random_string(length=12)
        send_mail(
            'Confirmation code',
            f'Your confirmation code is: {confirmation_code}',
            EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        user, created = User.objects.get_or_create(email=email, username=username)
        user.confirmation_code = confirmation_code
        user.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        try:
            user = User.objects.get(username=username, confirmation_code=confirmation_code)

            user.confirmation_code = ''
            user.save()
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Invalid username or confirmation code.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'username'

    def get_permissions(self):
        if self.action == 'user_creat':
            permission_classes = [CastomAdminSuperUser]
        if self.action == 'user_list':
            permission_classes = [CastomAdminSuperUser]
        if self.action == 'user_destroy':
            permission_classes = [CastomAdminSuperUser]
        if self.action == 'user_retrieve':
            permission_classes = [CastomAdminSuperUser]
        if self.action == 'patch_me_user':
            permission_classes = [UserUpdateRole]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def user_list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

 
    def user_create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.data.get('username') == 'me':
            raise AssertionError()
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def user_retrieve(self, request, username):
        user = get_object_or_404(self.queryset, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def user_destroy(self, request, username):
        instance = User.objects.get(username=username)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def user_patch(self, request, username=None):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='me')
    def me_user(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @me_user.mapping.patch
    def patch_me_user(self, request):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = DefaultPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    pagination_class = DefaultPagination


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    pagination_class = DefaultPagination


class ReviewViewSet(viewsets.ModelViewSet):
    """Обработчик запросов к отзывам на произведения."""

    serializer_class = ReviewSerializer
    # permission_classes =

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title_id=title)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()


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
