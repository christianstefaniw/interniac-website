from pathlib import Path
import os
from dotenv import load_dotenv
import django_heroku
from django.urls import reverse_lazy
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG') == 'True'


ALLOWED_HOSTS = ['www.interniac.org',
                 'www.interniac.herokuapp.com', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'notifications',
    'phonenumber_field',
    'nocaptcha_recaptcha',
    'defender',
    'accounts',
    'aboutus',
    'careers',
    'marketplace',
    'authentication',
    'home',
    'applications',
    'interniac_admin'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'defender.middleware.FailedLoginMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'connect_x.urls'

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

WSGI_APPLICATION = 'connect_x.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = reverse_lazy('login')

DJANGO_NOTIFICATIONS_CONFIG = {'SOFT_DELETE': True}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

AUTH_USER_MODEL = 'accounts.User'

CLOUDINARY_STORAGE = {'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'), 'API_KEY': os.getenv(
    'CLOUDINARY_API_KEY'), 'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'), }


DEFENDER_LOGIN_FAILURE_LIMIT = 10
DEFENDER_LOCKOUT_TEMPLATE = 'auth/login.html'

if not DEBUG:
    django_heroku.settings(locals())
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    DEFENDER_REDIS_URL = os.getenv('REDIS_URL')
    NORECAPTCHA_SITE_KEY = os.environ.get('NORECAPTCHA_SITE_KEY')
    NORECAPTCHA_SECRET_KEY = os.environ.get('NORECAPTCHA_SECRET_KEY')
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DNS'),
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True
    )
else:
    NORECAPTCHA_SITE_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
    NORECAPTCHA_SECRET_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
