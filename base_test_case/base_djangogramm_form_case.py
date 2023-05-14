from django.test import TestCase


class BaseDjangogrammFormsCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post_text = {
            'text': 'test post text'
        }
        cls.post_tag = {
            'tags': 'test tag'
        }
        cls.post_pic = {
            'picture': 'test_pic.jpg'
        }

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()
