from django import forms
from django.forms import FileInput
from django.utils.translation import gettext_lazy as _

from djangogramm_app.models import Avatar


class AvatarForm(forms.ModelForm):
    avatar = forms.ImageField(
        label=_('Picture',),
        widget=FileInput(attrs={'class': 'form-control-file'})
    )

    class Meta:
        model = Avatar
        fields = ('avatar',)
