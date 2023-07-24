from tests.base_test_case.base_case import BaseTestCase
from users import models
from users.repositories import FollowRepository


class TestFollowRepository(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.follow_repository = FollowRepository()

    def test_follow_model_property(self):
        self.assertEqual(self.follow_repository.model, models.Follow)

    def test_create_user_follow(self):
        follow = self.follow_repository.create(user=self.test_user, author=self.test_user_2)
        self.assertTrue(follow)

    def test_get_user_follow(self):
        self.follow_repository.create(user=self.test_user, author=self.test_user_2)
        exists_follow = self.follow_repository.get_user_follow(user=self.test_user, user_id=self.test_user_2)
        self.assertTrue(exists_follow)

    # def test_get_user_unfollow(self):
    #     self.follow_repository.create(user=self.test_user, author=self.test_user_2)
    #     self.follow_repository.get_unfollow_user(user=self.test_user, user_id=self.test_user_2)
    #     exists_follow = self.follow_repository.get_user_follow(user=self.test_user, user_id=self.test_user_2)
    #     self.assertFalse(exists_follow)
