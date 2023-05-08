from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode

from djangogramm_app.models import Pictures

User = get_user_model()


class TestDjangogrammViews(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.home = reverse('index')
        cls.register_url = reverse('register')
        cls.login_url = reverse('login')
        cls.logout_url = reverse('logout')
        cls.test_profile_settings = reverse('profile_settings')
        cls.avatar = Pictures.objects.create(pictures='test_pic.jpg')
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
        cls.test_verify = reverse('verify_email', args=[cls.test_uidb64, cls.test_token])
        cls.profile_url = reverse('profile', args=[cls.test_user.id])
        cls.update_profile_url = reverse('update_profile')
        cls.delete_profile_url = reverse('delete_profile', args=[cls.test_user.id])
        cls.profile_list_url = reverse('profile_list')
        cls.index = reverse('index')
        cls.post_create = reverse('post_create')
        cls.post_delete = reverse('post_delete')
        cls.post_like = reverse('post_like')
        cls.post_dislike = reverse('post_dislike')

    # TODO: finish tests for djnagogramm views
    # def test_post_GET(self):
    #     self.client.force_login(self.test_user)
    #     response = self.client.get(self.index)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'index.html')

    # def test_post_create_GET(self):
    #     self.client.force_login(self.test_user)
    #     response = self.client.get(self.post_create)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'posts/post_create.html')
