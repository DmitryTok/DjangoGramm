import os
import sys
from os import environ as env
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.get('SUPER_SECRET', default='django-insecure-qzb1y40)_a5q9#lf*hf_$lcbp+srju)7%(ussgj8+vc06uhw2r')

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'djangogramm_app',
    'cloudinary',
    'cloudinary_storage'
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

COVERAGE_MODULE_EXCLUDES = [
    'tests$',
    'settings$',
    'urls$',
    'locale$',
    'migrations$',
    'admin$',
]

ROOT_URLCONF = 'DjangoGramm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'DjangoGramm/templates')],
        'APP_DIRS': [
            'users',
            'djangogramm_app'
        ],
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

WSGI_APPLICATION = 'DjangoGramm.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': env.get('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': env.get('DB_NAME', default='djangogramm'),
        'USER': env.get('DB_USER', default='dmitry_tok'),
        'PASSWORD': env.get('DB_PASSWORD', default='postgres'),
        'HOST': env.get('DB_HOST', default='db'),
        'PORT': env.get('DB_PORT', default='5432'),
    },
    'test': {
        'ENGINE': env.get('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': env.get('TEST_DB_NAME', default='test_djangogramm'),
        'USER': env.get('DB_USER', default='dmitry_tok'),
        'PASSWORD': env.get('DB_PASSWORD', default='postgres'),
        'HOST': env.get('TEST_DB_HOST', default='test_db'),
        'PORT': env.get('TEST_DB_PORT', default='5432'),
    }
}

if 'test' in sys.argv:
    DATABASES['default'] = DATABASES['test']


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'users.User'

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env.get('GET_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.get('GET_EMAIL_HOST_PASSWORD')

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'DjangoGramm/media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TEST_DATABASE_PREFIX = 'test_'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env.get('CLOUDINARY_NAME', default='dfjmjzaw4'),
    'API_KEY': env.get('CLOUDINARY_API_KEY', default='894441351422764'),
    'API_SECRET': env.get('CLOUDINARY_API_SECRET', default='e2otD2CMGKrOCGQtHxI9cdz7LGE')
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
