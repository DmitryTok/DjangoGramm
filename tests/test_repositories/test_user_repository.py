from base_test_case.base_case import BaseTestCase
from users import models


class TestUsersRepository(BaseTestCase):

    def test_user_model_property(self):
        self.assertEqual(self.user_repository.model, models.User)

    def test_user_repository_get(self):
        users = self.user_repository.get()
        all_users = models.User.objects.all()
        self.assertEqual(list(users), list(all_users))

    def test_get_user_id(self):
        user = self.user_repository.get_user_id(self.test_user.id)
        self.assertEqual(user.id, self.test_user.id)

    def test_request_user(self):
        request_user = self.user_repository.get_request_user(self.test_request)
        self.assertEqual(request_user.id, self.test_user_2.id)

    def test_delete_user(self):
        self.user_repository.delete_user_by_id(self.test_user.id)
        self.assertFalse(models.User.objects.filter(id=self.test_user.id).exists())

    def test_exclude_user(self):
        result = self.user_repository.exclude_user(self.test_request)
        self.assertNotIn(self.test_user_2, result)
        self.assertIn(self.test_user, result)

    def test_get_uid_user(self):
        result = self.user_repository.get_user(self.test_uidb64)
        self.assertIsNotNone(result)
