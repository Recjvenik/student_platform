"""
Django settings for Student Training & Job Platform POC
"""

from pathlib import Path
import os

from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # Third party apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    
    # Local apps
    'accounts',
    'students',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),     
        'PASSWORD': config('DB_PASSWORD'),  
        'HOST': config('DB_HOST'),  # Host
        'PORT': config('DB_PORT', default=5432, cast=int),  # Default PostgreSQL port (as it's not specified in the URL)
        'OPTIONS': {
            'sslmode': 'require',  # SSL mode parameter
            'channel_binding': 'require',  # Channel binding parameter
        }
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'




# Django-allauth settings
# Django-allauth settings
SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Updated Allauth settings for newer versions
# Login methods configuration
ACCOUNT_LOGIN_METHODS = {'email'}  # Only email login

# Signup fields configuration (for social auth only, no standard signup)
ACCOUNT_SIGNUP_FIELDS = ['email']  # Include email in signup fields

# Remove these deprecated settings:
# ACCOUNT_EMAIL_REQUIRED = False  # REMOVE THIS
# ACCOUNT_USERNAME_REQUIRED = False  # REMOVE THIS
# ACCOUNT_USER_MODEL_USERNAME_FIELD = None  # REMOVE THIS (or set to 'email' if needed)

# Email configuration
ACCOUNT_EMAIL_VERIFICATION = 'none'  # Since you're using OTP/social auth
ACCOUNT_EMAIL_REQUIRED = True  # Keep this but set to True for social accounts

# Social account settings
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True

# Redirect settings
LOGIN_REDIRECT_URL = '/profile/start/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Google OAuth settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'APP': {
            'client_id': config('GOOGLE_CLIENT_ID'),
            'secret': config('GOOGLE_SECRET'),
            'key': ''
        },
    }
}

# Redis configuration for OTP storage
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Session configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# OTP Settings
OTP_EXPIRY_SECONDS = 90

TWO_FACTOR_API_KEY = config('TWO_FACTOR_API_KEY')


