from DjangoGramm.Base.base_test_case.base_case import BaseTestCase
from djangogramm_app import models
from djangogramm_app.repositories import PictureRepository


class TestPictureRepository(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pic_repository = PictureRepository()
        cls.pic_data = {'picture': 'test_picture.jpg'}

    def test_pic_model_property(self):
        self.assertEqual(self.pic_repository.model, models.Pictures)

    def test_pic_create_with_get_or_create(self):
        avatar, created = self.pic_repository.create(use_get_or_create=True, **self.pic_data)
        self.assertTrue(created)
        self.assertEqual(avatar.picture, 'test_picture.jpg')

    def test_pic_create_without_get_or_create(self):
        pic = self.pic_repository.create(use_get_or_create=False, **self.pic_data)
        self.assertEqual(pic.picture, 'test_picture.jpg')
