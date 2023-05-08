from django.test import TestCase

from djangogramm_app.models import Pictures
from users.models import User


class TestUsersModels(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.avatar = Pictures.objects.create(
            picture='test_image.jpg'
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

    def test_user_model(self):
        user = User.objects.get(id=self.test_user.id)
        self.assertEqual(user.email, 'test_user@example.com')
        self.assertEqual(user.username, 'test_user')
        self.assertEqual(user.full_name, 'test_user')
        self.assertEqual(user.bio, 'This is a test bio.')
        self.assertEqual(user.avatar, self.avatar)
        self.assertTrue(user.is_email_verify)
