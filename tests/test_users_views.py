from base_test_case.base_user_case import BaseUserTestCase


class TestUsersViews(BaseUserTestCase):

    def test_registration_GET(self):
        response = self.guest_client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertContains(response, 'Email:')
        self.assertNotContains(response, 'Unexpected field')

    def test_registration_POST(self):
        response = self.guest_client.post(self.register_url, data=self.anonim_user)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertContains(response, 'testuser')
        self.assertNotContains(response, 'unexpected_test_user')

    def test_login_GET(self):
        response = self.guest_client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'Email address:')
        self.assertNotContains(response, 'unexpected field')

    def test_login_POST(self):
        response = self.guest_client.post(self.login_url, self.test_user_login)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email address:')
        self.assertNotContains(response, 'unexpected field')

    def test_login_POST_wrong_password(self):
        response = self.guest_client.post(self.login_url, self.test_user_not_exists)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email address:')
        self.assertNotContains(response, 'unexpected field')

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
        self.assertContains(response, 'Add some more info')
        self.assertNotContains(response, 'Dont add some more info')

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
        self.assertContains(response, 'Email: test_user@example.com')
        self.assertNotContains(response, 'Email: not_test_user@example.com')

        anon_response = self.guest_client.get(self.profile_url)
        self.assertEqual(anon_response.status_code, 302)
        self.assertRedirects(anon_response, self.login_url)

    def test_update_profile_GET(self):
        response = self.authorized_client.get(self.update_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/update_profile.html')
        self.assertContains(response, 'Update Profile')
        self.assertNotContains(response, 'Dont Update Profile')

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
        self.assertContains(response, 'Confirm to delete profile: test_user')
        self.assertNotContains(response, 'Confirm to delete profile: not_test_user')

    def test_delete_profile_POST(self):
        response = self.authorized_client.post(self.delete_profile_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home)

    def test_all_profiles_GET(self):
        response = self.authorized_client.get(self.profile_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile_list.html')
        self.assertContains(response, 'All Djangogramm Users')
        self.assertNotContains(response, 'Not All Djangogramm Users')
