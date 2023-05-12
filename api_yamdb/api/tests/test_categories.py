from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from reviews.models import User, Category


class TestMyAPI(APITestCase):
    """Тестирование ресурса Категории (Categories)."""

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
        cls.category = Category.objects.create(
            name='test_category',
            slug='category_slug'
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

    def test_anon_user_view_categories(self):
        """
        Анонимный пользователь
        может получать данные из GET запроса к ресурсу categories.
        """

        url = reverse('api:categories-list')
        response = self.anon_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_view_categories(self):
        """
        Авторизированный пользователь
        может получать данные из GET запроса к ресурсу categories.
        """

        url = reverse('api:categories-list')
        response = self.user_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_only_admin_can_add_categories(self):
        """Только Админ может добавлять новые категории"""

        url = reverse('api:categories-list')
        category_1 = {'name': 'category_1', 'slug': 'category_1_slug', }
        category_2 = {'name': 'category_2', 'slug': 'category_2_slug', }

        response = self.anon_client.post(url, category_1)
        self.assertEqual(response.status_code, 401)

        response = self.user_client.post(url, category_1)
        self.assertEqual(response.status_code, 403)

        response = self.moderator_client.post(url, category_1)
        self.assertEqual(response.status_code, 403)

        response = self.admin_client.post(url, category_1)
        self.assertEqual(response.status_code, 201)

        response = self.superuser_client.post(url, category_2)
        self.assertEqual(response.status_code, 201)

    def test_only_admin_can_delete_categories(self):
        """Только Админ может удалять категории"""

        url = reverse('api:categories-detail',
                      kwargs={'slug': self.category.slug})

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
