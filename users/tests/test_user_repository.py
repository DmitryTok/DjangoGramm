from django.http import HttpRequest
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from tests.base_test_case.base_case import BaseTestCase
from users import models
from users.repositories import FollowRepository, UserRepository


class TestUsersRepository(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_repository = UserRepository()
        cls.follow_repository = FollowRepository()
        cls.test_uidb64 = urlsafe_base64_encode(force_bytes(cls.test_user.pk))
        cls.test_request = HttpRequest()
        cls.test_request.user = cls.test_user_2
        cls.test_uid = str(cls.test_user.id)
        cls.anonim_user = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        cls.User = models.User

    def test_user_model_property(self):
        self.assertEqual(self.user_repository.model, models.User)

    def test_user_create(self):
        user_count_before = self.User.objects.count()
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
        }
        created_user, _ = self.user_repository.create(**user_data)
        user_count_after = self.User.objects.count()

        self.assertEqual(user_count_after, user_count_before + 1)
        self.assertEqual(created_user.username, user_data['username'])
        self.assertEqual(created_user.email, user_data['email'])

    def test_user_repository_get(self):
        users = self.user_repository.get()
        all_users = models.User.objects.all()
        self.assertEqual(list(users), list(all_users))

    def test_get_user_id(self):
        user = self.user_repository.get_user_id(self.test_user.id)
        self.assertEqual(user.id, self.test_user.id)

    def test_request_user(self):
        request_user = self.user_repository.get_request_user(self.test_request)
        self.assertEqual(request_user.id, self.test_user_2.id)

    def test_delete_user(self):
        self.user_repository.delete_user_by_id(self.test_user.id)
        self.assertFalse(models.User.objects.filter(id=self.test_user.id).exists())

    def test_exclude_user(self):
        result = self.user_repository.exclude_user(self.test_request)
        self.assertNotIn(self.test_user_2, result)
        self.assertIn(self.test_user, result)

    def test_get_uid_user(self):
        result = self.user_repository.get_user(self.test_uidb64)
        self.assertIsNotNone(result)

    def test_get_followers_of_author(self):
        self.follow_repository.create(user=self.test_user, author=self.test_user_2)
        result = self.user_repository.get_followers_of_author(self.test_user_2)
        self.assertIn(self.test_user, result)
        self.assertNotIn(self.test_user_2, result)

    def test_get_count_followers_of_author(self):
        self.follow_repository.create(user=self.test_user, author=self.test_user_2)
        result = self.user_repository.get_count_followers_of_author(self.test_user_2)
        self.assertEqual(result, 1)

    def test_get_user_follow(self):
        self.follow_repository.create(user=self.test_user, author=self.test_user_2)
        result = self.follow_repository.get_user_follow(self.test_user.id, self.test_user_2.id)
        self.assertTrue(result)

    # def test_get_unfollow_user(self):
    #     self.follow_repository.create(user=self.test_user, author=self.test_user_2)
    #     self.follow_repository.get_unfollow_user(self.test_user, self.test_user_2)
    #     result = self.follow_repository.get_user_follow(self.test_user.id, self.test_user_2.id)
    #     self.assertEqual(result, 0)
