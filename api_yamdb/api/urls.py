from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenVerifyView,
)
from .views import UserViewSet, signup, token


router = routers.SimpleRouter()


# Пользователи
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    # path('v1/auth/signup/', TokenObtainPairView.as_view(), 
    #      name='token_obtain_pair'),
    path('v1/auth/signup/', signup, 
          name='signup'),
    path('v1/auth/token/', token, 
          name='token'),
    path('v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('v1/', include(router.urls)),
]