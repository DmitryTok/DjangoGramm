import json

from django.contrib.auth.tokens import default_token_generator
from django.core.paginator import Page
from django.http import HttpRequest
from django.utils.http import urlsafe_base64_encode

from tests.base_test_case.base_case import BaseTestCase
from users.repositories import FollowRepository


class TestUsersViews(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_request = HttpRequest()
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
            'email': 'test_user@example.com',
            'password': 'testpasswordnotexists'
        }
        cls.test_uidb64 = urlsafe_base64_encode(str(cls.test_user.pk).encode()).rstrip('=')
        cls.test_token = default_token_generator.make_token(cls.test_user)
        cls.profile_data = {
            'full_name': 'Updated Name',
            'bio': 'Updated bio.',
            'avatar': 'image.jpg'
        }
        cls.test_request.user = cls.test_user_2
        cls.test_uid = str(cls.test_user.id)

    def test_registration_GET(self):
        response = self.guest_client.get(self.get_url(self.register_url))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertContains(response, 'Email:')
        self.assertNotContains(response, 'Unexpected field')

    def test_registration_POST(self):
        response = self.guest_client.post(self.get_url(self.register_url), data=self.anonim_user)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertContains(response, 'testuser')
        self.assertNotContains(response, 'unexpected_test_user')

    def test_login_GET(self):
        response = self.guest_client.get(self.get_url(self.login_url))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'Email address:')
        self.assertNotContains(response, 'unexpected field')

    def test_login_POST(self):
        response = self.guest_client.post(self.get_url(self.login_url), data=self.test_user_login)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'Email address:')
        self.assertNotContains(response, 'unexpected field')

    def test_login_POST_wrong_password(self):
        response = self.guest_client.post(self.get_url(self.login_url), data=self.test_user_not_exists)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email address:')
        self.assertNotContains(response, 'unexpected field')

    def test_logout_GET(self):
        response = self.guest_client.get(self.get_url(self.logout_url))
        self.assertEqual(response.status_code, 302)

    def test_email_verification_GET(self):
        response = self.guest_client.get(self.get_url(self.test_verify, self.test_uidb64, self.test_token))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.get_url(self.test_profile_settings))
        self.test_user.refresh_from_db()
        self.assertTrue(self.test_user.is_email_verify)

    def test_email_verification_invalid_token(self):
        response = self.guest_client.get(self.get_url(self.test_verify, self.test_uidb64, 'invalid-token'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.get_url(self.test_invalid_verify))

    def test_profile_settings_GET(self):
        response = self.authorized_client.get(self.get_url(self.test_profile_settings))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile_settings.html')
        self.assertContains(response, 'Add some more info')
        self.assertNotContains(response, 'Dont add some more info')

    def test_profile_settings_POST(self):
        response = self.authorized_client.post(self.get_url(self.test_profile_settings), data=self.profile_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.get_url(self.profile_url, self.test_user.id))

    def test_profile_GET(self):
        response = self.authorized_client.get(self.get_url(self.profile_url, self.test_user.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
        self.assertContains(response, 'Email: test_user@example.com')
        self.assertNotContains(response, 'Email: not_test_user@example.com')

        anon_response = self.guest_client.get(self.get_url(self.profile_url, self.test_user.id))
        self.assertEqual(anon_response.status_code, 302)
        self.assertRedirects(anon_response, self.get_url(self.login_url))

    def test_update_profile_GET(self):
        response = self.authorized_client.get(self.get_url(self.update_profile_url))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/update_profile.html')
        self.assertContains(response, 'Update Profile')
        self.assertNotContains(response, 'Dont Update Profile')

        anon_response = self.guest_client.get(self.get_url(self.update_profile_url))
        self.assertEqual(anon_response.status_code, 302)
        self.assertRedirects(anon_response, self.get_url(self.login_url))

    def test_update_profile_POST(self):
        response = self.authorized_client.post(self.get_url(self.update_profile_url), data=self.profile_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.get_url(self.home))

        anon_response = self.guest_client.get(self.get_url(self.update_profile_url))
        self.assertEqual(anon_response.status_code, 302)
        self.assertRedirects(anon_response, self.get_url(self.login_url))

    def test_delete_profile_GET(self):
        response = self.authorized_client.get(self.get_url(self.delete_profile_url, self.test_user.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/delete_profile.html')
        self.assertContains(response, 'Confirm to delete profile: test_user')
        self.assertNotContains(response, 'Confirm to delete profile: not_test_user')

    def test_delete_profile_POST(self):
        response = self.authorized_client.post(self.get_url(self.delete_profile_url, self.test_user.id))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.get_url(self.home))

    def test_all_profiles_GET(self):
        response = self.authorized_client.get(self.get_url(self.profile_list_url))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile_list.html')
        self.assertContains(response, 'All Djangogramm Users')
        self.assertNotContains(response, 'Not All Djangogramm Users')

        anon_response = self.guest_client.get(self.get_url(self.profile_list_url))
        self.assertEqual(anon_response.status_code, 302)
        self.assertRedirects(anon_response, self.get_url(self.login_url))

    def test_follow_user_POST(self):
        response = self.authorized_client.post(self.get_url(self.profile_follow, self.test_user_2.id))
        self.assertEqual(response.status_code, 201)

        anon_response = self.guest_client.post(self.get_url(self.profile_follow, self.test_user_2.id))
        self.assertEqual(anon_response.status_code, 400)

        anon_response_data = json.loads(anon_response.content.decode('utf-8'))
        self.assertEqual(anon_response_data['message'], 'You must be logged in to view this page')

    def test_unfollow_user_POST(self):
        self.authorized_client.post(self.get_url(self.profile_follow, self.test_user_2.id))
        response = self.authorized_client.post(self.get_url(self.profile_unfollow, self.test_user_2.id))
        self.assertEqual(response.status_code, 204)

        anon_response = self.guest_client.post(self.get_url(self.profile_unfollow, self.test_user_2.id))
        self.assertEqual(anon_response.status_code, 400)

        anon_response_data = json.loads(anon_response.content.decode('utf-8'))
        self.assertEqual(anon_response_data['message'], 'You must be logged in to view this page')

    def test_all_followers_user_GET(self):
        follow_repository = FollowRepository()
        follow_repository.create(user=self.test_user_2, author=self.test_user)
        response = self.authorized_client.get(self.get_url(self.profile_followers, self.test_user.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile_followers.html')
        self.assertContains(response, 'Followers')
        self.assertNotContains(response, 'Unfollowers')
        self.assertIsInstance(response.context['page_obj'], Page)
        self.assertEqual(response.context['page_obj'].number, 1)
        self.assertIn(self.test_user_2, response.context['all_followers'])
        self.assertNotIn(self.test_user, response.context['all_followers'])

        anon_response = self.guest_client.get(self.get_url(self.profile_followers, self.test_user.id))
        self.assertEqual(anon_response.status_code, 302)
        self.assertRedirects(anon_response, self.get_url(self.login_url))
