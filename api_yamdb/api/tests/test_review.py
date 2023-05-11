from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from review.models import (User, Genre, Category, Title,
                           Review, Comment, GenreTitle)


class TestMyAPI(APITestCase):
    """Тестирование ресурса Отзывы (Review)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin = User.objects.create_superuser(
            username='admin',
            password='password',
            email='admin@example.com'
        )
        cls.user = User.objects.create_user(
            username='user',
            password='password',
            email='user@example.com',
            role='user'
        )
        cls.moderator = User.objects.create_user(
            username='user',
            password='password',
            email='user@example.com',
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
            year=2025,
            genre=cls.genre,
            category=cls.category
        )
        cls.review = Review.objects.create(
            title=cls.title,
            author= cls.user,
            text='review',
            score=8
            )

    def setUp(self):
        self.user_client = APIClient()
        self.anon_client = APIClient()
        self.admin_client = APIClient()
        self.moderator_client = APIClient()
        self.admin_client.force_authenticate(self.admin)
        self.admin_client.force_authenticate(self.moderator)
        self.user_client.force_authenticate(self.user)


    def test_anon_user_access_to_review(self):
        """Анонимный пользователь может получать данные из GET запроса."""

        urls = (
            (reverse('api:review-list'), status.HTTP_200_OK),
            (reverse('api:review-detail', kwargs={'pk': self.review})))

        for url, expected_status_code in urls:
            with self.subTest(url=url, status_code=expected_status_code):
                response = self.anon_client.get(url)
                self.assertEqual(response.status_code,
                                 expected_status_code)

    def test_auth_user_access_to_review(self):
        """Авторизованный пользователь может получать данные из GET запроса."""

        urls = (
            (reverse('api:review-list'), status.HTTP_200_OK),
            (reverse('api:review-detail', kwargs={'pk': self.review})))

        for url, expected_status_code in urls:
            with self.subTest(url=url, status_code=expected_status_code):
                response = self.moderator_client.get(url)
                self.assertEqual(response.status_code,
                                 expected_status_code)

    def test_anon_user_cant_post_review(self):
        """Создать отзыв может только авторизованный пользователь."""
        data = {
            'title': self.title,
            'score': 10,
            'text': 'test',
        }
        response = self.anon_client.post(reverse('api:review-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.moderator_client.post(reverse('api:review-list'),
                                              data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_edit_request_for_post(self):
        """Изменять запись может только автор, администратор и админ."""
        data = {
            'score': 1,
            'text': 'test_1',
        }
        new_user = User.objects.create_user(
            username='user_1',
            password='password',
            email='user@example_1.com',
            role='user'
        )
        new_user_client = APIClient()
        new_user_client.force_authenticate(new_user_client)

        response = new_user_client.put(
            reverse('api:review-detail', kwargs={'pk': 1}), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.anon_client.put(
            reverse('api:review-detail', kwargs={'pk': 1}), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.admin_client.put(
            reverse('api:review-detail', kwargs={'pk': 1}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.moderator_client.put(
            reverse('api:review-detail', kwargs={'pk': 1}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.user_client.put(
            reverse('api:review-detail', kwargs={'pk': 1}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.user_client.delete(
            reverse('api:post-detail', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.moderator_client.delete(
            reverse('api:review-detail', kwargs={'pk': 1}), data=data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.admin_client.delete(
            reverse('api:review-detail', kwargs={'pk': 1}), data=data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
