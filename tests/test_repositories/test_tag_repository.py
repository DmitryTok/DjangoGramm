from base_test_case.base_case import BaseTestCase
from djangogramm_app import models


class TestTagRepository(BaseTestCase):

    def test_tag_model_property(self):
        self.assertEqual(self.tag_repository.model, models.Tag)

    def test_tag_create_with_get_or_create(self):
        tag, created = self.tag_repository.create(use_get_or_create=True, **self.tag_data)
        self.assertTrue(created)
        self.assertEqual(tag.name, 'Test Tag')

    def test_tag_create_without_get_or_create(self):
        tag = self.tag_repository.create(use_get_or_create=False, **self.tag_data)
        self.assertIsNotNone(tag.id)
        self.assertEqual(tag.name, 'Test Tag')
