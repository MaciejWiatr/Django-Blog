import sys
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.mail import send_mail
from django_blog.email_config import EMAIL_HOST_USER


def file_path_gen(instance, filename):
    file = filename
    class_name = instance.__class__.__name__
    slug = instance.title
    file_type = "media" if file.endswith(('.png', '.jpg', '.jpeg')) else "files"

    return f'{class_name}/{slug}/{file_type}/{file}'

    # return f'post/{instance.slug}/{filename}'


def compress_image(uploadedImage):
    image_temporary = Image.open(uploadedImage)
    outputIoStream = BytesIO()
    image_temproary_resized = image_temporary.resize((1020, 573))
    if image_temporary.mode != 'RGB':
        try:
            image_temporary = pure_pil_alpha_to_color_v2(image_temporary)
        except IndexError:
            pass
        image_temporary = image_temporary.convert('RGB')
    image_temporary.save(outputIoStream, format='JPEG', quality=80)
    outputIoStream.seek(0)
    uploadedImage = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % uploadedImage.name.split('.')[0],
                                         'image/jpeg', sys.getsizeof(outputIoStream), None)
    return uploadedImage


def pure_pil_alpha_to_color_v2(image, color=(255, 255, 255)):
    image.load()  # needed for split()
    background = Image.new('RGB', image.size, color)
    background.paste(image, mask=image.split()[3])  # 3 is the alpha channel
    return background


def send_newsletter_confirmation(Subscription, site_url):
    send_mail(
        "Potwierdzenie subskrypcji",
        "Cześć,\nWłaśnie dołączyłeś do newslettera na moim blogu!, od teraz będziesz otrzymywał powiadomienie o "
        "każdym nowym artykule :) \nPozdrawiam\nMaciej Wiatr"
        f"\nSwoją subskrypcję możesz anulować pod adresem: {site_url}newsletter/delete/{Subscription.code}"
        ,
        EMAIL_HOST_USER,
        [Subscription.email, ],
        fail_silently=False
    )


def send_post_notification(Post, site_url, subs):
    url = site_url.split('post/create')[0]
    send_mail(
        f"Nowy wpis na blogu - {Post.title}",
        "Cześć, właśnie ukazał się nowy wpis na moim blogu!\n"
        f"Możesz go przeczytać pod adresem:\n{url}post/detail/{Post.slug}/\n"
        "Pozdrawiam\n"
        "Maciej Wiatr\n",
        EMAIL_HOST_USER,
        subs,
        fail_silently=False

    )
