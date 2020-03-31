import os
import shutil
from pathlib import Path
from django.template.defaultfilters import slugify
from .models import Post, NewsletterSubscription
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django_blog.settings import MEDIA_ROOT, BASE_DIR
from django.utils.crypto import get_random_string


@receiver(post_delete, sender=Post)
def clear_files(sender, instance, **kwargs):
    media_path = MEDIA_ROOT + f'/{instance.__class__.__name__}/{instance.title}/'
    print(f'Trying to delete {media_path}')
    if os.path.exists(media_path):
        root = Path(BASE_DIR)
        directory = Path(media_path)
        if root in directory.parents:  # Extra safety option to guarantee safety to files outside django dir
            print(f'Deleting media folder: {media_path}')
            try:
                shutil.rmtree(media_path)
                print('Successfully deleted media folder')
            except Exception as e:
                print(f'An error occured during folder deletion {e}')
        else:
            print('Folder is in incorrect path')
    else:
        print('Folder dont exist')


@receiver(post_save, sender=Post)
def create_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


@receiver(post_save, sender=NewsletterSubscription)
def create_code(sender, instance, **kwargs):
    if not instance.code:
        instance.code = f'{instance.pk}{get_random_string(length=10)}'
        instance.save()
