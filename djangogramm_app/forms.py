from django import forms

from djangogramm_app.models import Pictures, Post, Tag


class PostForm(forms.ModelForm):
    text = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Post
        exclude = ('user', 'tags', 'likes', 'pictures', 'dislikes')


class TagForm(forms.ModelForm):
    tags = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        help_text='Example: first_tag, second_tag, third_tag...',
    )

    class Meta:
        model = Tag
        fields = ('tags',)


class PictureFormPost(forms.ModelForm):
    picture = forms.ImageField(
        label='Images',
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False
    )

    class Meta:
        model = Pictures
        fields = ('picture',)
