"""Модели для работы с базой данных."""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint


class Review(models.Model):
    """Модель отзывов на произведения."""

    title_id = models.IntegerField()
    text = models.TextField(
        verbose_name='Текст отзыва',
        max_length=5000,
    )
    author = models.IntegerField()
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
            UniqueConstraint(fields=('title_id', 'author'),
                             name='unique_title_id_and_author')
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    """Модель комментариев к отзывам."""

    review_id = models.ForeignKey(
        to='Review',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    author = models.IntegerField()
    text = models.TextField(
        max_length=500,
        verbose_name='Текст',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]
