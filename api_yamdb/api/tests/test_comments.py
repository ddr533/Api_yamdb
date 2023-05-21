from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from reviews.models import Category, Comment, Genre, Review, Title, User


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
            author=cls.user,
            text='review',
            score=8
        )
        cls.comment = Comment.objects.create(
            review=cls.review,
            author=cls.user,
            text='comment',
        )

    def setUp(self):
        self.user_client = APIClient()
        self.anon_client = APIClient()
        self.admin_client = APIClient()
        self.moderator_client = APIClient()
        self.admin_client.force_authenticate(self.admin)
        self.moderator_client.force_authenticate(self.moderator)
        self.user_client.force_authenticate(self.user)

    def test_anon_user_access_to_comments(self):
        """Анонимный пользователь может получать данные из GET запроса."""
        urls = (
            (reverse('api:comments-list',
                     kwargs={'title_id': self.title.id,
                             'review_id': self.review.id}),
             status.HTTP_200_OK),
            (reverse('api:comments-detail',
                     kwargs={'title_id': self.title.id,
                             'review_id': self.review.id,
                             'pk': self.comment.id}),
             status.HTTP_200_OK)
        )

        for url, expected_status_code in urls:
            with self.subTest(url=url, status_code=expected_status_code):
                response = self.anon_client.get(url)
                self.assertEqual(response.status_code,
                                 expected_status_code)

    def test_auth_user_access_to_comments(self):
        """Авторизованный пользователь может получать данные из GET запроса."""
        urls = (
            (reverse('api:comments-list',
                     kwargs={'title_id': self.title.id,
                             'review_id': self.review.id}),
             status.HTTP_200_OK),
            (reverse('api:comments-detail',
                     kwargs={'title_id': self.title.id,
                             'review_id': self.review.id,
                             'pk': self.comment.id}),
             status.HTTP_200_OK)
        )

        for url, expected_status_code in urls:
            with self.subTest(url=url, status_code=expected_status_code):
                response = self.moderator_client.get(url)
                self.assertEqual(response.status_code,
                                 expected_status_code)

    def test_anon_user_cant_post_comments(self):
        """Комметировать может только авторизованный пользователь."""
        data = {
            'review': self.review,
            'text': 'comment_1',
        }
        url = reverse('api:comments-list', kwargs={
            'title_id': self.title.id,
            'review_id': self.review.id})
        response = self.anon_client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.moderator_client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_comments_for_post(self):
        """Изменять комментрий может только автор, администратор и админ."""
        url = reverse('api:comments-detail',
                      kwargs={'title_id': self.title.id,
                              'review_id': self.review.id,
                              'pk': self.comment.id})
        data = {'text': 'update_comment_1'}
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

    def test_moderator_can_del_comment(self):
        """Модератор может удалить комментарий."""
        url = reverse('api:comments-detail',
                      kwargs={'title_id': self.title.id,
                              'review_id': self.review.id,
                              'pk': self.comment.id})
        response = self.moderator_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_can_del_comment(self):
        """Админ может удалить комментарий."""
        url = reverse('api:comments-detail',
                      kwargs={'title_id': self.title.id,
                              'review_id': self.review.id,
                              'pk': self.comment.id})
        response = self.admin_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
