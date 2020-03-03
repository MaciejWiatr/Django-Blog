import sys
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


def file_path_gen(instance, filename):
    file = filename
    class_name = instance.__class__.__name__
    slug = instance.slug if instance.slug else instance.title if instance.title else instance.id
    file_type = "media" if file.endswith(('.png', '.jpg', '.jpeg')) else "files"

    return f'{class_name}/{slug}/{file_type}/{file}'

    # return f'post/{instance.slug}/{filename}'


def compress_image(uploadedImage):
    imageTemproary = Image.open(uploadedImage)
    outputIoStream = BytesIO()
    imageTemproaryResized = imageTemproary.resize((1020, 573))
    imageTemproary.save(outputIoStream, format='JPEG', quality=60)
    outputIoStream.seek(0)
    uploadedImage = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % uploadedImage.name.split('.')[0],
                                         'image/jpeg', sys.getsizeof(outputIoStream), None)
    return uploadedImage
