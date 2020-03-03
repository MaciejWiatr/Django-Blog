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
    try:
        imageTemproary = pure_pil_alpha_to_color_v2(imageTemproary)
    except:
        pass
    imageTemproary.save(outputIoStream, format='JPEG', quality=80)
    outputIoStream.seek(0)
    uploadedImage = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % uploadedImage.name.split('.')[0],
                                         'image/jpeg', sys.getsizeof(outputIoStream), None)
    return uploadedImage


def pure_pil_alpha_to_color_v2(image, color=(255, 255, 255)):
    image.load()  # needed for split()
    background = Image.new('RGB', image.size, color)
    background.paste(image, mask=image.split()[3])  # 3 is the alpha channel
    return background
