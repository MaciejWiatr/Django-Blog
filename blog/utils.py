def file_path_gen(instance, filename):
    file = filename
    class_name = instance.__class__.__name__
    slug = instance.slug if instance.slug else instance.title if instance.title else instance.id
    file_type = "media" if file.endswith(('.png', '.jpg', '.jpeg')) else "files"

    return f'{class_name}/{slug}/{file_type}/{file}'
    # return f'post/{instance.slug}/{filename}'
