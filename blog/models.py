from django.db import models

# Create your models here.
from django.template.defaultfilters import slugify
from django.urls import reverse


def img_path(instance, filename):
    return f'post/{instance.title}/{filename}'


class Post(models.Model):
    title = models.CharField(max_length=20, blank=False)
    text = models.TextField(max_length=256)
    image = models.ImageField(upload_to=img_path)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        print(self.title + "saved")
        if not self.slug:
            self.slug = slugify(self.title)
        print(self.slug)
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
