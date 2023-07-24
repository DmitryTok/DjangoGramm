from djangogramm_app.models import Post
from tests.base_test_case.base_case import BaseTestCase


class TestPostViews(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_post = {
            'user': cls.test_user,
            'text': 'Test post text',
            'pub_date': '2023-05-04 12:00:00',
            'pictures': cls.picture,
            'tags': cls.tag
        }
        cls.post = Post.objects.create(
            user=cls.test_user,
            text='Test post text',
            pub_date='2023-05-04 12:00:00'
        )
        cls.post.pictures.add(cls.picture)
        cls.post.tags.add(cls.tag)
        cls.post.likes.add(cls.test_user)
        cls.post.dislikes.add(cls.test_user_2)

    def test_post_GET(self):
        response = self.authorized_client.get(self.get_url(self.home))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Test post text')
        self.assertNotContains(response, 'Not test post text')

        anon_response = self.guest_client.get(self.get_url(self.home))
        self.assertEqual(anon_response.status_code, 200)
        self.assertTemplateUsed(anon_response, 'index.html')
        self.assertContains(anon_response, 'Test post text')
        self.assertNotContains(anon_response, 'Not test post text')

    def test_post_create_GET(self):
        response = self.authorized_client.get(self.get_url(self.post_create))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_create.html')
        self.assertContains(response, 'Create Post')
        self.assertNotContains(response, 'Not Create Post')

        anon_response = self.guest_client.get(self.get_url(self.post_create))
        self.assertEqual(anon_response.status_code, 302)
        self.assertRedirects(anon_response, self.get_url(self.login_url))

    def test_post_create_POST(self):
        response = self.authorized_client.post(self.get_url(self.post_create), data=self.create_post)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.get_url(self.home))

        anon_response = self.guest_client.post(self.get_url(self.post_create), data=self.create_post)
        self.assertEqual(anon_response.status_code, 302)
        self.assertRedirects(anon_response, self.get_url(self.login_url))

    def test_post_delete_GET(self):
        response = self.authorized_client.get(self.get_url(self.post_delete, self.post.id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Confirm to delete Post: Test post text')
        self.assertNotContains(response, 'Confirm to delete Post: Unexpected post')

        anon_response = self.guest_client.post(self.get_url(self.post_delete, self.post.id))
        self.assertEqual(anon_response.status_code, 302)
        self.assertRedirects(anon_response, self.get_url(self.login_url))

    def test_post_delete_POST(self):
        response = self.authorized_client.post(self.get_url(self.post_delete, self.post.id))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.get_url(self.profile_url, self.test_user.id))

        anon_response = self.guest_client.post(self.get_url(self.post_delete, self.test_user.id))
        self.assertEqual(anon_response.status_code, 404)

    def test_post_like_POST(self):
        response = self.authorized_client.post(self.get_url(self.post_like, self.post.id))
        self.assertEqual(response.status_code, 200)

        anon_response = self.guest_client.post(self.get_url(self.post_like, self.post.id))
        self.assertEqual(anon_response.status_code, 400)

    def test_post_dislike_POST(self):
        response = self.authorized_client.post(self.get_url(self.post_dislike, self.post.id))
        self.assertEqual(response.status_code, 200)

        anon_response = self.guest_client.post(self.get_url(self.post_dislike, self.post.id))
        self.assertEqual(anon_response.status_code, 400)
