from django.db import models


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
    genre = models.ManyToManyField(Genre, through='GenreTitle',
                                   null=True)
    category = models.ForeignKey(
        Category, related_name='titles', on_delete=models.SET_NULL,
        null=True)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Таблица отношений (многие-ко-многим) жанров и произведений"""
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
