from ckeditor.fields import RichTextField
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from taggit.managers import TaggableManager
from .utils import file_path_gen, compress_image


class Post(models.Model):
    title = models.CharField(max_length=64, blank=False)
    text = RichTextField()
    image = models.ImageField(upload_to=file_path_gen, default="no-img.png")
    slug = models.SlugField(null=False, unique=True)
    files = models.FileField(upload_to=file_path_gen, null=True, blank=True)
    tags = TaggableManager()

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.id:
            self.image = compress_image(self.image)
        # super(Post, self).save(*args, **kwargs)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=128)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment nr.{self.id} | {self.text[:10]}"
