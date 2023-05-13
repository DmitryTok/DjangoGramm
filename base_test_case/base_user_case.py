from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode

from djangogramm_app.models import Pictures

User = get_user_model()


class BaseUserTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.home = reverse('index')
        cls.register_url = reverse('register')
        cls.login_url = reverse('login')
        cls.logout_url = reverse('logout')
        cls.test_profile_settings = reverse('profile_settings')
        cls.avatar = Pictures.objects.create(picture='test_image.jpg')
        cls.anonim_user = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        cls.test_user_login = {
            'email': 'test_user@example.com',
            'password': 'testpassword'
        }
        cls.test_user_not_exists = {
            'email': 'test_user_not_exists@example.com',
            'password': 'testpasswordnotexists'
        }
        cls.test_user = User.objects.create_user(
            email='test_user@example.com',
            username='test_user',
            full_name='test_user',
            bio='This is a test bio.',
            is_email_verify=True
        )
        cls.authorized_client.force_login(cls.test_user)
        cls.test_user.avatar = cls.avatar
        cls.test_user.save()
        cls.test_uidb64 = urlsafe_base64_encode(str(cls.test_user.pk).encode()).rstrip('=')
        cls.test_token = default_token_generator.make_token(cls.test_user)
        cls.test_verify = reverse('verify_email', args=[cls.test_uidb64, cls.test_token])
        cls.profile_url = reverse('profile', args=[cls.test_user.id])
        cls.update_profile_url = reverse('update_profile')
        cls.delete_profile_url = reverse('delete_profile', args=[cls.test_user.id])
        cls.profile_list_url = reverse('profile_list')

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()
