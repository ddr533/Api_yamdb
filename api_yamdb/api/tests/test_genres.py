from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from reviews.models import Genre, User


class TestMyAPI(APITestCase):
    """Тестирование ресурса Жанры (Genres)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.superuser = User.objects.create_superuser(
            username='superuser',
            password='password',
            email='superuser@example.com',
        )
        cls.admin = User.objects.create_user(
            username='admin',
            password='password',
            email='admin@example.com',
            role='admin'
        )
        cls.user = User.objects.create_user(
            username='user_test',
            password='password',
            email='user@example_1.com',
            role='user'
        )
        cls.moderator = User.objects.create_user(
            username='user_mod',
            password='password',
            email='user@example_2.com',
            role='moderator'
        )
        cls.genre = Genre.objects.create(
            name='test_genre',
            slug='genre_slug'
        )

    def setUp(self):
        self.user_client = APIClient()
        self.anon_client = APIClient()
        self.superuser_client = APIClient()
        self.admin_client = APIClient()
        self.moderator_client = APIClient()
        self.superuser_client.force_authenticate(self.superuser)
        self.admin_client.force_authenticate(self.admin)
        self.moderator_client.force_authenticate(self.moderator)
        self.user_client.force_authenticate(self.user)

    def test_anon_user_view_genres(self):
        """
        Анонимный пользователь
        может получать данные из GET запроса к ресурсу genres.
        """

        url = reverse('api:genres-list')
        response = self.anon_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_view_genres(self):
        """
        Авторизированный пользователь
        может получать данные из GET запроса к ресурсу genres.
        """

        url = reverse('api:genres-list')
        response = self.user_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_only_admin_can_add_genres(self):
        """Только Админ может добавлять новые жанры"""

        url = reverse('api:genres-list')
        genre_1 = {'name': 'new_genre_1', 'slug': 'new_genre_1_slug', }
        genre_2 = {'name': 'new_genre_2', 'slug': 'new_genre_2_slug', }

        response = self.anon_client.post(url, genre_1)
        self.assertEqual(response.status_code, 401)

        response = self.user_client.post(url, genre_1)
        self.assertEqual(response.status_code, 403)

        response = self.moderator_client.post(url, genre_1)
        self.assertEqual(response.status_code, 403)

        response = self.admin_client.post(url, genre_1)
        self.assertEqual(response.status_code, 201)

        response = self.superuser_client.post(url, genre_2)
        self.assertEqual(response.status_code, 201)

    def test_only_admin_can_delete_genres(self):
        """Только Админ может удалять жанры"""

        url = reverse('api:genres-detail', kwargs={'slug': self.genre.slug})

        response = self.anon_client.post(url)
        self.assertEqual(response.status_code, 401)

        response = self.user_client.post(url)
        self.assertEqual(response.status_code, 403)

        response = self.moderator_client.post(url)
        self.assertEqual(response.status_code, 403)

        response = self.admin_client.delete(url)
        self.assertEqual(response.status_code, 204)

        response = self.superuser_client.delete(url)
        self.assertEqual(response.status_code, 404)
