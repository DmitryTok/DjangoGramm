from base_test_case.base_case import BaseTestCase
from djangogramm_app import models


class TestPictureRepository(BaseTestCase):

    def test_pic_model_property(self):
        self.assertEqual(self.pic_repository.model, models.Pictures)

    def test_pic_create_with_get_or_create(self):
        avatar, created = self.pic_repository.create(use_get_or_create=True, **self.pic_data)
        self.assertTrue(created)
        self.assertEqual(avatar.picture, 'test_picture.jpg')

    def test_pic_create_without_get_or_create(self):
        pic = self.pic_repository.create(use_get_or_create=False, **self.pic_data)
        self.assertIsNotNone(pic.id)
        self.assertEqual(pic.picture, 'test_picture.jpg')
