from django.test import TestCase

from djangogramm_app.forms import PictureFormPost, PostForm, TagForm


class TestDjangogrammForms(TestCase):

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

    def test_post_form_valid(self):
        form = PostForm(data=self.post_text)
        self.assertTrue(form.is_valid())

    def test_post_form_not_valid(self):
        form = PostForm(data={})
        self.assertFalse(form.is_valid())

    def test_tag_form_valid(self):
        form = TagForm(data=self.post_tag)
        self.assertTrue(form.is_valid())

    def test_tag_form_empty_valid(self):
        form = TagForm(data={})
        self.assertTrue(form.is_valid())

    def test_picture_form_valid(self):
        form = PictureFormPost(data=self.post_pic)
        self.assertTrue(form.is_valid())

    def test_picture_form_empty_valid(self):
        form = PictureFormPost(data={})
        self.assertTrue(form.is_valid())
