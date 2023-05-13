from django.db import IntegrityError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from reviews.models import User


class TestMyAPIUser(APITestCase):
    """Тестирование пользователей."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com'
        )
        cls.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com'
        )
        cls.data = {
            "username": "string",
            "email": "user@example.com",
            "first_name": "string",
            "last_name": "string",
            "bio": "string",
            "role": "user"
        }

    def setUp(self):
        self.admin_client = APIClient()
        self.user_client = APIClient()
        self.admin_client.force_authenticate(self.admin)
        self.user_client.force_authenticate(self.user)

    def test_admin_get_list_all_users(self):
        """Получить список всех пользователей. Права доступа: Администратор."""
        url = reverse('api:user-list')
        response = self.admin_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_post_add_new_user(self):
        """Добавить нового пользователя. Права доступа: Администратор."""
        url = reverse('api:user-list')
        response = self.admin_client.post(url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_post_add_new_user_with_name_me(self):
        """Добавить нового пользователя с именем me нельзя.
         Права доступа: Администратор."""
        url = reverse('api:user-list')
        data = {'username': 'me', 'email': 'testuser@example.com'}
        response = self.admin_client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_get_all_name_username(self):
        """Получить пользователя по username. Права доступа: Администратор."""
        url = reverse('api:user-detail', args=[self.user.username])
        response = self.admin_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_patch_update_name_username(self):
        """Изменить данные пользователя по username.
         Права доступа: Администратор."""
        url = reverse('api:user-detail', args=[self.user.username])
        data = {'first_name': 'new_name'}
        response = self.admin_client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'new_name')

    def test_admin_delete_name_username(self):
        """Удалить пользователя по username. Права доступа: Администратор."""
        url = reverse('api:user-detail', args=[self.user.username])
        response = self.admin_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_user_with_invalid_data(self):
        """ Попытка создания пользователя который уже есть в базе."""
        invalid_data = {'username': 'new_user',
                        'email': 'testuser@example.com',
                        }
        with self.assertRaises(IntegrityError):
            User.objects.create_user(**invalid_data)
