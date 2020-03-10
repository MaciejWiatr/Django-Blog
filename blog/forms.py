from ckeditor.widgets import CKEditorWidget
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.template.defaultfilters import slugify

from .models import Comment, Post


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'comment-text'})
        }


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'files', 'tags']
        widgets = {
            'text': forms.CharField(widget=CKEditorWidget())
        }

    def clean_title(self):  # If given title already exists function throws an error
        title = self.cleaned_data.get('title')
        slug = slugify(title)
        slugs = [post.slug for post in Post.objects.all()]
        if slug in slugs:
            raise ValidationError("Taki tytuł już istnieje")
        else:
            return title
