"""Модели для работы с базой данных."""

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import UniqueConstraint
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
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.get_full_name() or self.username


      
class Category(models.Model):
    """Категории (типы) произведений."""
    
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    """Жанры произведений."""
    
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    """Произведения в базе данных."""
    
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category, related_name='titles', on_delete=models.SET_NULL,
        null=True)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Таблица отношений (многие-ко-многим) жанров и произведений."""
    
    genre = models.ForeignKey(Genre, related_name='genre', on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    """Модель отзывов на произведения."""

    title = models.ForeignKey(
        to=Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        max_length=5000,
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)])
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date', '-id')
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            UniqueConstraint(fields=('title', 'author'),
                             name='unique_title_and_author')
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    """Модель комментариев к отзывам."""

    review = models.ForeignKey(
        to='Review',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )
    text = models.TextField(
        max_length=500,
        verbose_name='Текст',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date', '-id')
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]
