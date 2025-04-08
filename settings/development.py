from .base import *


ALLOWED_HOSTS = ["127.0.0.1", "localhost", "task-manager-a1ma.onrender.com"]

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
