from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True if os.getenv('DEBUG') == 'True' else False

ALLOWED_HOSTS = [host for host in os.getenv('ALLOWED_HOSTS', '').split(',') if host] or ['*']
CSRF_TRUSTED_ORIGINS = [host for host in os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',') if host]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Library:
    
    # My apps:
    'users',
    'table_reservation',
    'core'
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# ---------------------- Настройки базы данных ----------------------
DATABASES = {
    'default': dj_database_url.parse(
        os.getenv('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
} if os.getenv('DATABASE_URL') else {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('HOST'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}
# -------------------------------------------------------------------


# ------------- Настройки аутентификации пользователя ---------------
# Валидаторы сложности пароля
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

LOGIN_REDIRECT_URL = 'core:home'

LOGOUT_REDIRECT_URL = 'core:home'

LOGIN_URL = 'users:login'
# -------------------------------------------------------------------


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ------------------- Настройки почтового сервиса -------------------
# Если SMTP-переменные не заданы, письма пишутся в консоль
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_SERVICES = {}

if os.getenv('EMAIL_HOST_MAIN'):
    EMAIL_SERVICES['main'] = {
        'HOST': os.getenv('EMAIL_HOST_MAIN'),
        'PORT': int(os.getenv('EMAIL_PORT_MAIN')),
        'USER': os.getenv('EMAIL_HOST_USER_MAIN'),
        'PASSWORD': os.getenv('EMAIL_HOST_PASSWORD_MAIN'),
        'USE_TLS': os.getenv('EMAIL_USE_TLS_MAIN') == 'True',
        'USE_SSL': os.getenv('EMAIL_USE_SSL_MAIN') == 'True',
    }

if os.getenv('EMAIL_HOST_AUTO'):
    EMAIL_SERVICES['auto'] = {
        'HOST': os.getenv('EMAIL_HOST_AUTO'),
        'PORT': int(os.getenv('EMAIL_PORT_AUTO')),
        'USER': os.getenv('EMAIL_HOST_USER_AUTO'),
        'PASSWORD': os.getenv('EMAIL_HOST_PASSWORD_AUTO'),
        'USE_TLS': os.getenv('EMAIL_USE_TLS_AUTO') == 'True',
        'USE_SSL': os.getenv('EMAIL_USE_SSL_AUTO') == 'True',
    }

if not EMAIL_SERVICES:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Главную почту используем по умолчанию
SERVER_EMAIL = EMAIL_SERVICES.get('main', {}).get('USER', 'noreply@localhost')
DEFAULT_FROM_EMAIL = EMAIL_SERVICES.get('main', {}).get('USER', 'noreply@localhost')
# -------------------------------------------------------------------
