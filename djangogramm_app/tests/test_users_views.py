from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode

from djangogramm_app.models import Pictures

User = get_user_model()


class TestUsersViews(TestCase):
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

    def test_registration_GET(self):
        response = self.guest_client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_registration_POST(self):
        response = self.guest_client.post(self.register_url, data=self.anonim_user)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_login_GET(self):
        response = self.guest_client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_POST(self):
        response = self.guest_client.post(self.login_url, self.test_user_login)
        self.assertEqual(response.status_code, 200)

    def test_login_POST_wrong_password(self):
        response = self.guest_client.post(self.login_url, self.test_user_not_exists)
        self.assertEqual(response.status_code, 200)

    def test_logout_GET(self):
        response = self.guest_client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)

    def test_email_verification_GET(self):
        response = self.guest_client.get(self.test_verify)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.test_profile_settings)
        self.test_user.refresh_from_db()
        self.assertTrue(self.test_user.is_email_verify)

    def test_profile_settings_GET(self):
        response = self.authorized_client.get(self.test_profile_settings)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile_settings.html')

    def test_profile_settings_POST(self):
        data = {
            'full_name': 'test_user',
            'bio': 'This is a test bio.',
            'avatar': self.avatar
        }
        response = self.authorized_client.post(self.test_profile_settings, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.profile_url)

    def test_profile_GET(self):
        response = self.authorized_client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

        anon_response = self.guest_client.get(self.profile_url)
        self.assertEqual(anon_response.status_code, 302)
        self.assertRedirects(anon_response, self.login_url)

    def test_update_profile_GET(self):
        response = self.authorized_client.get(self.update_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/update_profile.html')

        anon_response = self.guest_client.get(self.update_profile_url)
        self.assertEqual(anon_response.status_code, 302)
        self.assertRedirects(anon_response, self.login_url)

    def test_update_profile_POST(self):
        data = {
            'full_name': 'Updated Name',
            'bio': 'Updated bio.',
            'avatar': 'updated_pic.jpg'
        }
        response = self.authorized_client.post(self.update_profile_url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home)

        anon_response = self.guest_client.get(self.update_profile_url)
        self.assertEqual(anon_response.status_code, 302)
        self.assertRedirects(anon_response, self.login_url)

    def test_delete_profile_GET(self):
        response = self.authorized_client.get(self.delete_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/delete_profile.html')

    def test_delete_profile_POST(self):
        response = self.authorized_client.post(self.delete_profile_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home)

    def test_all_profiles_GET(self):
        response = self.authorized_client.get(self.profile_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile_list.html')
