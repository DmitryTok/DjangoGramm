from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ClearableFileInput, EmailInput, Textarea, TextInput
from django.utils.translation import gettext_lazy as _

from djangogramm_app.models import Avatar
from users.models import User
from users.utils import send_email_for_verify


class CustomAuthenticationForm(AuthenticationForm):

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if not self.user_cache.is_email_veryfi:
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
        widget=EmailInput(attrs={'autocomlete': 'email'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',)


class ProfileForm(forms.ModelForm):
    username = forms.CharField(
        label=_('Username'),
        max_length=50,
        widget=TextInput(attrs={'class': 'form-control'})
    )
    full_name = forms.CharField(
        label=_('Full name'),
        max_length=50,
        widget=TextInput(attrs={'class': 'form-control'})
    )
    bio = forms.CharField(
        label=_('Bio'),
        max_length=1500,
        widget=Textarea(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'full_name', 'bio')


class AvatarForm(forms.ModelForm):
    avatar = forms.ImageField(
        label=_('Avatar'),
        widget=ClearableFileInput(attrs={'multiple': False})
    )

    class Meta:
        model = Avatar
        fields = ('avatar',)
