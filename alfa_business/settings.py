import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-*!%icz1z4cq&k#4zy$+xowg#p$#z@%_4fsa6gtc8flo#7h4s^)')
DEBUG = True  # Убедитесь, что DEBUG=True для разработки
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'business_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'alfa_business.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# НАСТРОЙКИ СТАТИЧЕСКИХ ФАЙЛОВ - исправьте эту часть
STATIC_URL = '/static/'

# Для разработки
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Для продакшена (пока не нужно)
STATIC_ROOT = BASE_DIR / "staticfiles"

# Медиа файлы (если понадобятся)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')