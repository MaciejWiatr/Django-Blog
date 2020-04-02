from ckeditor.fields import RichTextField
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager
from .utils import file_path_gen, compress_image
from .managers import PostManager, CommentManager, NewsletterManager


class Post(models.Model):
    title = models.CharField(max_length=64, blank=False)
    text = RichTextField()
    image = models.ImageField(upload_to=file_path_gen, default="no-img.png")
    slug = models.SlugField(null=False, unique=True)
    files = models.FileField(upload_to=file_path_gen, null=True, blank=True)
    pub_date = models.DateTimeField('date created', default=timezone.now)
    tags = TaggableManager()
    objects = PostManager()

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.image = compress_image(self.image)  # Signals somehow dont seem to work in image compression case :/
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('blog:post_delete', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('blog:post_update', kwargs={'slug': self.slug})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    objects = CommentManager()

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment nr.{self.id} | {self.text[:10]}"

    def get_delete_url(self):
        return reverse('blog:activate_comment', kwargs={'action': 'delete', 'pk': self.pk})

    def get_activate_url(self):
        return reverse('blog:activate_comment', kwargs={'action': 'activate', 'pk': self.pk})


class NewsletterSubscription(models.Model):
    email = models.EmailField(max_length=255)
    active = models.BooleanField(default=True)
    join_date = models.DateTimeField('date created', default=timezone.now)
    code = models.CharField(blank=True, max_length=10)
    objects = NewsletterManager()

    def get_unsub_mail(self):
        return reverse('blog:newsletter_unsub', kwargs={'code': self.code})

    def __str__(self):
        return self.email
