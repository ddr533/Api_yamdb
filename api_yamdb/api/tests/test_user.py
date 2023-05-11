from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from reviews.models import (User, Genre, Category, Title,
                           Review, Comment, GenreTitle)
from api_yamdb.settings import EMAIL_HOST_USER

class TestMyAPIUser(APITestCase):
    """Тестирование пользователей."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com'
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
        self.admin_client.force_authenticate(self.admin)


    def test_admin_get_list_all_users(self):
        """Получить список всех пользователей. Права доступа: Администратор."""
        url = reverse('api:user')
        response = self.admin_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_admin_post_add_new_user(self):
        """Добавить нового пользователя. Права доступа: Администратор."""
        url = reverse('api:user')
        response = self.admin_client.post(url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_get_all_name_username(self):
        """Получить пользователя по username. Права доступа: Администратор."""
        url = reverse('api:user-detail', args=[self.user.username])
        response = self.admin_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_patch_update_name_username(self):
        """Изменить данные пользователя по username. Права доступа: Администратор."""
        url = reverse('api:user', args=[self.user.username])
        data = {'first_name': 'new_name'}
        response = self.admin_client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'new_name')

    def test_admin_delete_name_username(self):
        """Удалить пользователя по username. Права доступа: Администратор."""
        url = reverse('api:user', args=[self.user.username])
        response = self.admin_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)