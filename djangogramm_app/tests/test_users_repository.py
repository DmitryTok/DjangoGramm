from django.http import HttpRequest
from django.test import TestCase

from djangogramm_app.models import Pictures, Tag
from users.models import User
from users.repositories import UserRepository


class TestUsersRepository(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_repository = UserRepository()
        cls.test_uidb64 = "valid_uidb64"
        cls.test_request = HttpRequest()
        cls.avatar = Pictures.objects.create(
            picture='test_image.jpg'
        )
        cls.tag = Tag.objects.create(
            name='test_tag'
        )
        cls.test_user = User.objects.create_user(
            email='test_user@example.com',
            username='test_user',
            full_name='test_user',
            bio='This is a test bio.',
            avatar=cls.avatar,
            is_email_verify=True
        )
        cls.test_user_2 = User.objects.create_user(
            email='test_user_2@example.com',
            username='test_user_2',
            full_name='test_user_2',
            bio='This is a test bio.',
            avatar=cls.avatar,
            is_email_verify=True
        )
        cls.test_request.user = cls.test_user_2
        cls.test_uid = str(cls.test_user.id)
        cls.pic_data = {'picture': 'test_picture.jpg'}

    def test_user_model_property(self):
        self.assertEqual(self.user_repository.model, User)

    def test_user_repository_get(self):
        users = self.user_repository.get()
        all_users = User.objects.all()
        self.assertEqual(list(users), list(all_users))

    def test_get_user_id(self):
        user = self.user_repository.get_user_id(self.test_user.id)
        self.assertEqual(user.id, self.test_user.id)

    def test_request_user(self):
        request_user = self.user_repository.get_request_user(self.test_request)
        self.assertEqual(request_user.id, self.test_user_2.id)

    def test_delete_user(self):
        self.user_repository.delete_user_by_id(self.test_user.id)
        self.assertFalse(User.objects.filter(id=self.test_user.id).exists())

    def test_exclude_user(self):
        result = self.user_repository.exclude_user(self.test_request)
        self.assertNotIn(self.test_user_2, result)
        self.assertIn(self.test_user, result)

    def test_get_uid_user(self):
        result = self.user_repository.get_user(self.test_uidb64)
        self.assertIsNone(result)
