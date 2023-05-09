from rest_framework import serializers
from reviews.models import User

class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=50)
    class Meta:
       fields = ['email', 'username'] 
       model = User

class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    confirmation_code = serializers.CharField(max_length=12)
    class Meta:
       fields = ['username', 'confirmation_code'] 
       model = User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'username', 
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
            ]
        model = User