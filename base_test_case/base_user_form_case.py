from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class BaseUserFormsCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.anon_user = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        cls.register_user = {
            'email': 'test_email@gmail.com',
            'username': 'tet_username',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
        cls.profile_settings = {
            'full_name': 'full_name',
            'bio': 'bio',
            'avatar': 'avatar.jpg'
        }
        cls.profile_settings_not_full = {
            'bio': 'bio',
        }
        cls.picture_data = {
            'picture': 'pic.jpg'
        }
        cls.user_update_data = {
            'username': 'new_username'
        }

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()
