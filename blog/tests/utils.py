import os
import shutil
from pathlib import Path

from django_blog.settings import MEDIA_ROOT, BASE_DIR


def clear_files():
    media_path = MEDIA_ROOT + f'/Post/TestPost/'
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
                print(f'An error occurred during folder deletion {e}')
        else:
            print('Folder is in incorrect path')
    else:
        print('Folder dont exist')
