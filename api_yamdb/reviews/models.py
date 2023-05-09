from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'Аутентифицированный пользователь'), 
        ('moderator', 'Модератор'), 
        ('admin', 'Администратор'),
    ]
    bio = models.TextField(null=True, blank=True)
    role = models.CharField(choices=ROLE_CHOICES, default='user',
                             max_length=30)
    confirmation_code = models.CharField(max_length=12, null=True, blank=True)

    def __str__(self):
        return self.get_full_name() or self.username
