from ckeditor.widgets import CKEditorWidget
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.template.defaultfilters import slugify

from .models import Comment, Post, NewsletterSubscription


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
        fields = ['image', 'title', 'tags', 'text', 'files']
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


class NewsletterForm(ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # if email in NewsletterSubscription.objects.email_list():
        #     raise ValidationError("Ten email już został zarejestrowany")
        return email
