from django.contrib.auth import get_user_model

from base_test_case.base_user_form_case import BaseUserFormsCase
from users.forms import CustomAuthenticationForm, PictureFormAvatar, ProfileForm, UserRegisterForm, UserUpdateForm

User = get_user_model()


class TestUserForms(BaseUserFormsCase):

    def test_auth_form_not_valid(self):
        form = CustomAuthenticationForm(data=self.anon_user)
        self.assertFalse(form.is_valid())

    def test_user_register_form_valid(self):
        form = UserRegisterForm(data=self.register_user)
        self.assertTrue(form.is_valid())

    def test_user_register_form_not_valid(self):
        form = UserRegisterForm(data=self.register_user)
        self.assertTrue(form.is_valid())

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
