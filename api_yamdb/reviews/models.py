"""Модели для работы с базой данных."""

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

MIN_REVIEW_SCORE = 1
MAX_REVIEW_SCORE = 10
SLICE_TEXT_FIELD = slice(0, 15)


class User(AbstractUser):
    """Пользователи."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (USER, 'Аутентифицированный пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )

    bio = models.TextField(null=True, blank=True, verbose_name='Биография')
    role = models.CharField(choices=ROLE_CHOICES,
                            default=USER,
                            max_length=30,
                            verbose_name='Роль')
    confirmation_code = models.CharField(max_length=12,
                                         null=True,
                                         blank=True,
                                         verbose_name='Код подтверждения')
    email = models.EmailField(unique=True)

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    class Meta:
        verbose_name = 'Пользователи'
        ordering = ('id', 'username')

    def __str__(self):
        return self.get_full_name() or self.username


class Category(models.Model):
    """Категории (типы) произведений."""

    name = models.CharField(max_length=256, verbose_name='Категория')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Категории'
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    """Жанры произведений."""

    name = models.CharField(max_length=256, verbose_name='Жанр')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Жанры'
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    """Произведения в базе данных."""

    name = models.CharField(max_length=256, verbose_name='Название')
    year = models.PositiveSmallIntegerField(verbose_name='Год', db_index=True)
    description = models.TextField(null=True, blank=True,
                                   verbose_name='Описание')
    genre = models.ManyToManyField(Genre, through='GenreTitle',
                                   verbose_name='Жанр')
    category = models.ForeignKey(
        Category, related_name='titles', on_delete=models.SET_NULL,
        null=True, verbose_name='Категория')

    class Meta:
        verbose_name = 'Произведение'
        ordering = ('name', 'year')

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Таблица отношений (многие-ко-многим) жанров и произведений."""

    genre = models.ForeignKey(Genre, related_name='genre',
                              on_delete=models.CASCADE, verbose_name='Жанр')
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              verbose_name='Произведение')

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    """Модель отзывов на произведения."""

    title = models.ForeignKey(
        to=Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        max_length=5000,
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(MIN_REVIEW_SCORE),
                    MaxValueValidator(MAX_REVIEW_SCORE)],
        verbose_name='Оценка'
    )
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
        return self.text[SLICE_TEXT_FIELD]


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
        on_delete=models.CASCADE,
        verbose_name='Автор'
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
        return self.text[SLICE_TEXT_FIELD]
