from base_test_case.base_case import BaseTestCase
from djangogramm_app import models


class TestPostRepositories(BaseTestCase):

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
