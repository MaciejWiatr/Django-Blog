from ckeditor.fields import RichTextField
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager
from .utils import file_path_gen, compress_image
from .managers import PostManager, CommentManager


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
            self.image = compress_image(self.image)  # Signals somehow dont seem to work in compression case :/
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=128)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    objects = CommentManager()

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment nr.{self.id} | {self.text[:10]}"
