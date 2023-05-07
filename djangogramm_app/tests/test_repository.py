from django.http import HttpRequest
from django.test import TestCase

from djangogramm_app.models import Pictures, Post, Tag
from djangogramm_app.repositories import PictureRepository, PostRepository, TagRepository
from users.models import User
from users.repositories import UserRepository


class RepositoryTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_uidb64 = "valid_uidb64"
        cls.test_request = HttpRequest()
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
        cls.test_request.user = cls.test_user_2
        cls.test_uid = str(cls.test_user.id)
        cls.post = Post.objects.create(
            user=cls.test_user,
            text='Test post text',
            pub_date='2023-05-04 12:00:00'
        )
        cls.post.pictures.add(cls.avatar)
        cls.post.tags.add(cls.tag)
        cls.post.likes.add(cls.test_user)
        cls.post.dislikes.add(cls.test_user_2)
        cls.user_repository = UserRepository()
        cls.post_repository = PostRepository()
        cls.tag_repository = TagRepository()
        cls.pic_repository = PictureRepository()
        cls.tag_data = {'name': 'Test Tag'}
        cls.pic_data = {'picture': 'test_picture.jpg'}

    def test_tag_model_property(self):
        self.assertEqual(self.tag_repository.model, Tag)

    def test_pic_model_property(self):
        self.assertEqual(self.pic_repository.model, Pictures)

    def test_post_model_property(self):
        self.assertEqual(self.post_repository.model, Post)

    def test_user_model_property(self):
        self.assertEqual(self.user_repository.model, User)

    def test_tag_create_with_get_or_create(self):
        tag, created = self.tag_repository.create(use_get_or_create=True, **self.tag_data)
        self.assertTrue(created)
        self.assertEqual(tag.name, 'Test Tag')

    def test_pic_create_with_get_or_create(self):
        avatar, created = self.pic_repository.create(use_get_or_create=True, **self.pic_data)
        self.assertTrue(created)
        self.assertEqual(avatar.picture, 'test_picture.jpg')

    def test_tag_create_without_get_or_create(self):
        tag = self.tag_repository.create(use_get_or_create=False, **self.tag_data)
        self.assertIsNotNone(tag.id)
        self.assertEqual(tag.name, 'Test Tag')

    def test_pic_create_without_get_or_create(self):
        pic = self.pic_repository.create(use_get_or_create=False, **self.pic_data)
        self.assertIsNotNone(pic.id)
        self.assertEqual(pic.picture, 'test_picture.jpg')

    def test_user_repository_get(self):
        users = self.user_repository.get()
        all_users = User.objects.all()
        self.assertEqual(list(users), list(all_users))

    def test_get_user_id(self):
        user = self.user_repository.get_user_id(self.test_user.id)
        self.assertEqual(user.id, 3)

    def test_request_user(self):
        request_user = self.user_repository.get_request_user(self.test_request)
        self.assertEqual(request_user.id, 4)

    def test_delete_user(self):
        self.user_repository.delete_user_by_id(self.test_user.id)
        self.assertFalse(User.objects.filter(id=self.test_user.id).exists())

    def test_exclude_user(self):
        result = self.user_repository.exclude_user(self.test_request)
        self.assertNotIn(self.test_user_2, result)
        self.assertIn(self.test_user, result)

    def test_get_uid_user(self):
        result = self.user_repository.get_user(self.test_uidb64)
        self.assertIsNone(result)

    def test_get_all_posts(self):
        posts = self.post_repository.get_all_posts()
        all_posts = Post.objects.all()
        self.assertEqual(list(posts), list(all_posts))

    def test_get_post_by_id(self):
        post = self.post_repository.get_post_by_id(self.post.id)
        self.assertEqual(post.id, 2)

    def test_delete_post_by_id(self):
        self.post_repository.delete_post_by_id(self.post.id)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_get_likes_or_dislikes(self):
        user_1 = self.test_user
        user_2 = self.test_user_2
        self.post.likes.add(user_1)
        self.post.dislikes.add(user_2)

        likes = self.post_repository.get_likes_or_dislikes(self.post.id, is_dislike=False)
        dislikes = self.post_repository.get_likes_or_dislikes(self.post.id, is_dislike=True)

        self.assertEqual(likes.count(), 1)
        self.assertEqual(dislikes.count(), 1)
