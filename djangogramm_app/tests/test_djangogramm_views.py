from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode

from djangogramm_app.models import Pictures, Post, Tag

User = get_user_model()


class TestDjangogrammViews(TestCase):
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
        cls.avatar = Pictures.objects.create(picture='test_pic.jpg')
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
        cls.authorized_client.force_login(cls.test_user)
        cls.post = Post.objects.create(
            user=cls.test_user,
            text='Test post text',
            pub_date='2023-05-04 12:00:00'
        )
        cls.create_post = {
            'user': cls.test_user,
            'text': 'Test post text',
            'pub_date': '2023-05-04 12:00:00',
            'pictures': cls.avatar,
            'tags': cls.tag
        }
        cls.post.pictures.add(cls.avatar)
        cls.post.tags.add(cls.tag)
        cls.post.likes.add(cls.test_user)
        cls.post.dislikes.add(cls.test_user_2)
        cls.test_uidb64 = urlsafe_base64_encode(str(cls.test_user.pk).encode()).rstrip('=')
        cls.test_token = default_token_generator.make_token(cls.test_user)
        cls.test_verify = reverse('verify_email', args=[cls.test_uidb64, cls.test_token])
        cls.profile_url = reverse('profile', args=[cls.test_user.id])
        cls.update_profile_url = reverse('update_profile')
        cls.delete_profile_url = reverse('delete_profile', args=[cls.test_user.id])
        cls.profile_list_url = reverse('profile_list')
        cls.index = reverse('index')
        cls.post_create = reverse('post_create')
        cls.post_delete = reverse('post_delete', args=[cls.post.id])
        cls.post_like = reverse('post_like', args=[cls.post.id])
        cls.post_dislike = reverse('post_dislike', args=[cls.post.id])

    def test_post_GET(self):
        response = self.authorized_client.get(self.index)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

        anon_response = self.guest_client.get(self.index)
        self.assertEqual(anon_response.status_code, 200)
        self.assertTemplateUsed(anon_response, 'index.html')

    def test_post_create_GET(self):
        response = self.authorized_client.get(self.post_create)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_create.html')

        anon_response = self.guest_client.get(self.post_create)
        self.assertEqual(anon_response.status_code, 302)
        self.assertRedirects(anon_response, self.login_url)

    def test_post_create_POST(self):
        response = self.authorized_client.post(self.post_create, data=self.create_post)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home)

        anon_response = self.guest_client.post(self.post_create, data=self.create_post)
        self.assertEqual(anon_response.status_code, 302)
        self.assertRedirects(anon_response, self.login_url)

    def test_post_delete_GET(self):
        response = self.authorized_client.get(self.post_delete)
        self.assertEqual(response.status_code, 200)

        anon_response = self.guest_client.post(self.post_delete)
        self.assertEqual(anon_response.status_code, 302)
        self.assertRedirects(anon_response, self.login_url)

    def test_post_delete_POST(self):
        response = self.authorized_client.post(self.post_delete)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.profile_url)

        anon_response = self.guest_client.post(self.post_delete)
        self.assertEqual(anon_response.status_code, 404)

    def test_post_like_POST(self):
        response = self.authorized_client.post(self.post_like)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home)

        anon_response = self.guest_client.post(self.post_like)
        self.assertEqual(anon_response.status_code, 302)
        self.assertRedirects(anon_response, self.login_url)

    def test_post_dislike_POST(self):
        response = self.authorized_client.post(self.post_dislike)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home)

        anon_response = self.guest_client.post(self.post_dislike)
        self.assertEqual(anon_response.status_code, 302)
        self.assertRedirects(anon_response, self.login_url)
