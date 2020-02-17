from django.db import models

# Create your models here.
from django.urls import reverse


def img_path(instance, filename):
    return f'post/{instance.title}/{filename}'


class Post(models.Model):
    title = models.CharField(max_length=20, blank=False)
    text = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to=img_path)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=128)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment nr.{self.id} | {self.text[:10]}"
