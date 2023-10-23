from .settings import *

INSTALLED_APPS = [
    "django.contrib.gis",
    "predictions_map",
]

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": BASE_DIR / "postgis",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
