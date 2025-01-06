# ...existing code...
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    # ...existing apps...
    # 'todos',
    'rest_framework',  # Add Django REST framework
]
# ...existing code...
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# ...existing code...
