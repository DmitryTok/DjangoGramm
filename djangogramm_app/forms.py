from django import forms

from djangogramm_app.models import Post, Tag


class PostForm(forms.ModelForm):
    text = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Post
        exclude = ('user', 'tags', 'likes')


class TagForm(forms.ModelForm):
    tags = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Tag
        fields = ('tags',)
