from djangogramm_app import models
from djangogramm_app.models import Post
from djangogramm_app.repositories import PostRepository
from tests.base_test_case.base_case import BaseTestCase


class TestPostRepositories(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post_repository = PostRepository()
        cls.create_post = {
            'user': cls.test_user,
            'text': 'Test post text',
            'pub_date': '2023-05-04 12:00:00',
            'pictures': cls.avatar,
            'tags': cls.tag
        }
        cls.post = Post.objects.create(
            user=cls.test_user,
            text='Test post text',
            pub_date='2023-05-04 12:00:00'
        )
        cls.post.pictures.add(cls.avatar)
        cls.post.tags.add(cls.tag)
        cls.post.likes.add(cls.test_user)
        cls.post.dislikes.add(cls.test_user_2)

    def test_post_model_property(self):
        self.assertEqual(self.post_repository.model, models.Post)

    def test_get_all_posts(self):
        posts = self.post_repository.get_all_posts()
        all_posts = models.Post.objects.all()
        self.assertEqual(list(posts), list(all_posts))

    def test_get_post_by_id(self):
        post = self.post_repository.get_post_by_id(self.post.id)
        self.assertEqual(post.id, self.post.id)

    def test_delete_post_by_id(self):
        self.post_repository.delete_post_by_id(self.post.id)
        self.assertFalse(models.Post.objects.filter(id=self.post.id).exists())

    def test_get_likes_or_dislikes(self):
        user_1 = self.test_user
        user_2 = self.test_user_2
        self.post.likes.add(user_1)
        self.post.dislikes.add(user_2)

        likes = self.post_repository.get_likes_or_dislikes(self.post.id, is_dislike=False)
        dislikes = self.post_repository.get_likes_or_dislikes(self.post.id, is_dislike=True)

        self.assertEqual(likes.count(), 1)
        self.assertEqual(dislikes.count(), 1)
