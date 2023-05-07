from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode

from djangogramm_app.models import Pictures

User = get_user_model()


class TestAuth(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.register_url = reverse('register')
        cls.login_url = reverse('login')
        cls.logout_url = reverse('logout')
        cls.avatar = Pictures.objects.create(
            picture='test_image.jpg'
        )
        cls.anonim_user = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        cls.test_user = User.objects.create_user(
            email='test_user@example.com',
            username='test_user',
            full_name='test_user',
            bio='This is a test bio.',
            avatar=cls.avatar,
            is_email_verify=True
        )
        cls.test_uidb64 = urlsafe_base64_encode(str(cls.test_user.pk).encode()).rstrip('=')
        cls.test_token = default_token_generator.make_token(cls.test_user)

    def test_registration_view(self):
        response = self.client.post(self.register_url, data=self.anonim_user)
        self.assertEqual(response.status_code, 200)

    def test_email_verification_view(self):
        url = reverse('verify_email', args=[self.test_uidb64, self.test_token])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('profile_settings'))
        self.test_user.refresh_from_db()
        self.assertTrue(self.test_user.is_email_verify)
