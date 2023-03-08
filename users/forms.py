from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import EmailInput, FileInput, Textarea, TextInput
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
        widget=EmailInput(attrs={'autocomlete': 'email'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')


class ProfileForm(forms.ModelForm):
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
    avatar = forms.ImageField(
        widget=FileInput(attrs={'class': 'form-control-file'})
    )

    class Meta:
        model = User
        fields = ('full_name', 'bio', 'avatar')
