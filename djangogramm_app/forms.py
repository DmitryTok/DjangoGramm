from django import forms

from djangogramm_app.models import Pictures, Post, Tag


class PostForm(forms.ModelForm):
    text = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Post
        exclude = ('user', 'tags', 'likes', 'pictures')


class TagForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Tag
        fields = ('tags',)


class PictureFormPost(forms.ModelForm):
    picture = forms.ImageField(
        label='Images',
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )

    class Meta:
        model = Pictures
        fields = ('picture',)
