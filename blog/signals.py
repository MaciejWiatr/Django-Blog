import os
import shutil
from pathlib import Path
from django.template.defaultfilters import slugify
from .models import Post
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django_blog.settings import MEDIA_ROOT, BASE_DIR


@receiver(post_delete, sender=Post)
def clear_files(sender, instance, **kwargs):
    media_path = MEDIA_ROOT + f'/{instance.__class__.__name__}/{instance.slug}/'
    if os.path.exists(media_path):
        root = Path(BASE_DIR)
        directory = Path(media_path)
        if root in directory.parents:  # Extra safety option to guarantee safety to files outside django dir
            print(f'Deleting media folder: {media_path}')
            shutil.rmtree(media_path)


@receiver(post_save, sender=Post)
def create_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)
