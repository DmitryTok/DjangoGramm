from django.contrib.auth import get_user_model

from tests.base_test_case.base_case import BaseTestCase
from users.forms import CustomAuthenticationForm, PictureFormAvatar, ProfileForm, UserRegisterForm, UserUpdateForm

User = get_user_model()


class TestUserForms(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.anon_user = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        cls.register_user = {
            'email': 'test_email@gmail.com',
            'username': 'tet_username',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
        cls.profile_settings = {
            'full_name': 'full_name',
            'bio': 'bio',
            'avatar': 'avatar.jpg'
        }
        cls.profile_settings_not_full = {
            'bio': 'bio',
        }
        cls.picture_data = {
            'picture': 'pic.jpg'
        }
        cls.user_update_data = {
            'username': 'new_username'
        }

    def test_auth_form_not_valid(self):
        form = CustomAuthenticationForm(data=self.anon_user)
        self.assertFalse(form.is_valid())

    def test_user_register_form_valid(self):
        form_valid = UserRegisterForm(data=self.register_user)
        self.assertTrue(form_valid.is_valid())

        form_invalid = UserRegisterForm(data={
            'email': 'test_user@example.com',
            'username': 'testuser2',
            'password1': 'securepassword456',
            'password2': 'securepassword456',
        })
        self.assertFalse(form_invalid.is_valid())
        self.assertEqual(
            form_invalid.errors['email'],
            ['This email is already registered. Please try to login or use a different email.']
        )

    def test_user_register_form_not_valid(self):
        form = UserRegisterForm(data={})
        self.assertFalse(form.is_valid())

    def test_profile_form_valid(self):
        form = ProfileForm(data=self.profile_settings)
        self.assertTrue(form.is_valid())

    def test_profile_form_valid_no_required_field(self):
        form = ProfileForm(data=self.profile_settings_not_full)
        self.assertTrue(form.is_valid())

    def test_picture_form_avatar_valid(self):
        form = PictureFormAvatar(data=self.picture_data)
        self.assertTrue(form.is_valid())

    def test_picture_form_avatar_empty_valid(self):
        form = PictureFormAvatar(data={})
        self.assertTrue(form.is_valid())

    def test_user_update_form_valid(self):
        form = UserUpdateForm(data=self.user_update_data)
        self.assertTrue(form.is_valid())

    def test_user_update_form_empty_valid(self):
        form = UserUpdateForm(data={})
        self.assertTrue(form.is_valid())
