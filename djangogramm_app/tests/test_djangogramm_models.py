from django.test import TestCase

from djangogramm_app.models import Pictures, Post, Tag
from users.models import User


class TestDjangogrammModels(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.avatar = Pictures.objects.create(
            picture='test_image.jpg'
        )
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
        cls.post = Post.objects.create(
            user=cls.test_user,
            text='Test post text',
            pub_date='2023-05-04 12:00:00'
        )
        cls.post.pictures.add(cls.avatar)
        cls.post.tags.add(cls.tag)
        cls.post.likes.add(cls.test_user)
        cls.post.dislikes.add(cls.test_user_2)

    def test_picture_model(self):
        pic = Pictures.objects.get(id=self.avatar.id)
        self.assertEqual(pic.picture, 'test_image.jpg')

    def test_tag_model(self):
        tag = Tag.objects.get(id=self.tag.id)
        self.assertEqual(tag.name, 'test_tag')

    def test_post_model(self):
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(post.user, self.test_user)
        self.assertEqual(post.text, 'Test post text')
        self.assertEqual(post.pictures.first(), self.avatar)
        self.assertEqual(post.tags.first(), self.tag)
        self.assertEqual(post.likes_count(), 1)
        self.assertEqual(post.dislikes_count(), 1)
        self.assertEqual(post.likes.first(), self.test_user)
