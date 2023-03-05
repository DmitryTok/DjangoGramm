from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from users.utils import send_email_for_verify

User = get_user_model()


class CustomAuthenticationForm(AuthenticationForm):

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if not self.user_cache.is_email_verify:
                send_email_for_verify(self.request, self.user_cache)
                raise ValidationError(
                    'Email is not verify, please check your email address',
                    code='invalid_login',
                )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        label=_('Email'),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomlete': 'email'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')


class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(max_length=70)
    bio = forms.CharField(max_length=1200)
    avatar = forms.ImageField()

    class Meta:
        model = User
        fields = ('full_name', 'bio', 'avatar')
        labels = {
            'full_name': 'Your full name',
            'bio': 'Few interesting things about you',
            'avatar': 'Your avatar image'}
        help_texts = {
            'full_name': 'Enter full name',
            'bio': 'Enter bio',
            'avatar': 'Upload avatar'
        }
