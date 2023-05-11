from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from reviews.models import (User, Genre, Category, Title,
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
            year=2025)

        cls.title.genre.set([cls.genre])


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
        self.moderator_client.force_authenticate(self.moderator)
        self.user_client.force_authenticate(self.user)


    def test_anon_user_access_to_review(self):
        """Анонимный пользователь может получать данные из GET запроса."""

        urls = (
            (reverse('api:reviews-list',
                     kwargs={'title_id': self.title.id}),
             status.HTTP_200_OK),
            (reverse('api:reviews-detail',
                     kwargs={'title_id': self.title.id, 'pk': self.review.id}),
             status.HTTP_200_OK)
        )

        for url, expected_status_code in urls:
            with self.subTest(url=url, status_code=expected_status_code):
                response = self.anon_client.get(url)
                self.assertEqual(response.status_code,
                                 expected_status_code)

    def test_auth_user_access_to_review(self):
        """Авторизованный пользователь может получать данные из GET запроса."""

        urls = (
            (reverse('api:reviews-list',
                     kwargs={'title_id': self.title.id}),
             status.HTTP_200_OK),
            (reverse('api:reviews-detail',
                     kwargs={'title_id': self.title.id, 'pk': self.review.id}),
             status.HTTP_200_OK))

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
        response = self.anon_client.post(
            reverse('api:reviews-list', kwargs={'title_id': self.title.id}),
            data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.moderator_client.post(
            reverse('api:reviews-list', kwargs={'title_id': self.title.id}),
            data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_edit_request_for_post(self):
        """Изменять отзыв может только автор, администратор и админ."""
        url = reverse('api:reviews-detail',
                    kwargs={'title_id': 1, 'pk': self.review.id})
        data = {
            'score': 1,
            'text': 'test_1',
        }
        new_user = User.objects.create_user(
            username='new_user',
            password='password',
            email='user@example_3.com',
            role='user'
        )
        new_user_client = APIClient()
        new_user_client.force_authenticate(new_user)

        response = new_user_client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.anon_client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.admin_client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.moderator_client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.user_client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.user_client.delete(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_moderator_can_del_review(self):
        """Модератор может удалить отзыв."""
        response = self.moderator_client.delete(reverse('api:reviews-detail',
                    kwargs={'title_id': 1, 'pk': self.review.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_can_del_review(self):
        """Админ может удалить отзыв."""
        response = self.admin_client.delete(reverse('api:reviews-detail',
                    kwargs={'title_id': 1, 'pk': self.review.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
