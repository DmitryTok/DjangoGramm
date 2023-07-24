from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from djangogramm_app.models import Pictures, Tag

User = get_user_model()


class BaseTestCase(TestCase):

    @staticmethod
    def get_url(route, *args):
        return reverse(route, args=args)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Created objects
        cls.picture = Pictures.objects.create(picture='test_pic.jpg')
        cls.avatar = Pictures.objects.create(avatar='test_avatar.jpg')
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
        cls.test_user.avatar = cls.avatar
        cls.test_user.save()

        # Clients
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.test_user)

        # URL
        cls.home = 'index'
        cls.register_url = 'register'
        cls.login_url = 'login'
        cls.logout_url = 'logout'
        cls.test_profile_settings = 'profile_settings'
        cls.test_verify = 'verify_email'
        cls.test_invalid_verify = 'invalid_verify'
        cls.profile_url = 'profile'
        cls.update_profile_url = 'update_profile'
        cls.delete_profile_url = 'delete_profile'
        cls.profile_list_url = 'profile_list'
        cls.post_create = 'post_create'
        cls.post_delete = 'post_delete'
        cls.post_like = 'post_like'
        cls.post_dislike = 'post_dislike'
        cls.profile_follow = 'profile_follow'
        cls.profile_unfollow = 'profile_unfollow'
        cls.profile_followers = 'profile_followers'

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()
