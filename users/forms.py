from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import EmailInput, Textarea, TextInput
from django.utils.translation import gettext_lazy as _

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
        fields = ('email', 'username')


class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(
        label=_('Full name'),
        max_length=50,
        required=False,
        widget=TextInput(attrs={'class': 'form-control'})
    )
    bio = forms.CharField(
        label=_('Bio'),
        max_length=1500,
        required=False,
        widget=Textarea(attrs={'class': 'form-control'})
    )
    avatar = forms.ImageField(
        label=_('Avatar'),
        required=False,
    )

    class Meta:
        model = User
        fields = ('full_name', 'bio', 'avatar')
