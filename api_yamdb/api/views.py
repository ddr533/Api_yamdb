from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken # удалить потом
from rest_framework_simplejwt.tokens import AccessToken
from django.utils.crypto import get_random_string
from reviews.models import User
from .serializers import UserSerializer, SignUpSerializer, TokenSerializer
from api_yamdb.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
# Create your views here.

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
            # user.confirmation_code = ''
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
    
