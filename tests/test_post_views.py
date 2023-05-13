from base_test_case.base_case import BaseTestCase


class TestPostView(BaseTestCase):

    def test_post_GET(self):
        response = self.authorized_client.get(self.index)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Test post text')
        self.assertNotContains(response, 'Not test post text')

        anon_response = self.guest_client.get(self.index)
        self.assertEqual(anon_response.status_code, 200)
        self.assertTemplateUsed(anon_response, 'index.html')
        self.assertContains(anon_response, 'Test post text')
        self.assertNotContains(anon_response, 'Not test post text')

    def test_post_create_GET(self):
        response = self.authorized_client.get(self.post_create)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_create.html')
        self.assertContains(response, 'Create Post')
        self.assertNotContains(response, 'Not Create Post')

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
        self.assertContains(response, 'Confirm to delete Post: Test post text')
        self.assertNotContains(response, 'Confirm to delete Post: Unexpected post')

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
