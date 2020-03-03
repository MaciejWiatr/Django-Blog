from ckeditor.widgets import CKEditorWidget
from django import forms
from django.forms import ModelForm

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
