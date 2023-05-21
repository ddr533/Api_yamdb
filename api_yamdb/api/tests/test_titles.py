from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from reviews.models import Category, Genre, Title, User


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
        cls.category = Category.objects.create(
            name='test_category',
            slug='category_slug'
        )

        cls.title = Title.objects.create(
            name='test_title',
            category=cls.category,
            year=2023)

        cls.title.genre.set([cls.genre])

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

    def test_anon_user_view_titles(self):
        """
        Анонимный пользователь
        может получать данные из GET запроса к ресурсу titles.
        """

        url = reverse('api:titles-list')
        response = self.anon_client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('api:titles-detail', kwargs={'pk': self.title.id})
        response = self.anon_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_view_genres(self):
        """
        Авторизированный пользователь
        может получать данные из GET запроса к ресурсу titles.
        """

        url = reverse('api:titles-list')
        response = self.user_client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('api:titles-detail', kwargs={'pk': self.title.id})
        response = self.user_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_only_admin_can_add_titles(self):
        """Только Админ может добавлять новые тайтлы"""

        url = reverse('api:titles-list')
        title_1 = {'name': 'new_title_1', 'category': self.category.slug,
                   'genre': self.genre.slug, 'year': 2023}
        title_2 = {'name': 'new_title_2', 'category': self.category.slug,
                   'genre': self.genre.slug, 'year': 2023}

        response = self.anon_client.post(url, title_1)
        self.assertEqual(response.status_code, 401)

        response = self.user_client.post(url, title_1)
        self.assertEqual(response.status_code, 403)

        response = self.moderator_client.post(url, title_1)
        self.assertEqual(response.status_code, 403)

        response = self.admin_client.post(url, title_1)
        self.assertEqual(response.status_code, 201)

        response = self.superuser_client.post(url, title_2)
        self.assertEqual(response.status_code, 201)

    def test_only_admin_can_delete_titles(self):
        """Только Админ может удалять тайтлы"""

        url = reverse('api:titles-detail', kwargs={'pk': self.title.id})

        response = self.anon_client.delete(url)
        self.assertEqual(response.status_code, 401)

        response = self.user_client.delete(url)
        self.assertEqual(response.status_code, 403)

        response = self.moderator_client.delete(url)
        self.assertEqual(response.status_code, 403)

        response = self.admin_client.delete(url)
        self.assertEqual(response.status_code, 204)

        response = self.superuser_client.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_only_admin_can_patch_titles(self):
        """Только Админ может редактировать тайтлы"""

        patch_request_1 = {'name': 'new_name_1'}
        patch_request_2 = {'name': 'new_name_2'}

        url = reverse('api:titles-detail', kwargs={'pk': self.title.id})

        response = self.anon_client.patch(url, patch_request_1)
        self.assertEqual(response.status_code, 401)

        response = self.user_client.patch(url, patch_request_1)
        self.assertEqual(response.status_code, 403)

        response = self.moderator_client.patch(url, patch_request_1)
        self.assertEqual(response.status_code, 403)

        response = self.admin_client.patch(url, patch_request_1)
        self.assertEqual(response.status_code, 200)

        response = self.superuser_client.patch(url, patch_request_2)
        self.assertEqual(response.status_code, 200)
