import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6jxvoqniu^ixyer6af-!#f$yo&s8$2-1vj)_g^@opgp&4x1x%!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'apps.core',
    'apps.reports',

    'registration',
    'widget_tweaks',
    'grappelli',
    'captcha',
    'django_csv_exports',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'manager.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'es'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGES = (
    ('es', _('Español'),),
    ('en', _('English'),),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
LOGIN_URL = reverse_lazy('auth_login')

REGISTRATION_AUTO_LOGIN = False
ACCOUNT_AUTHENTICATED_REGISTRATION_REDIRECTS = False
REGISTRATION_FORM = 'apps.core.forms.RegistrationForm'
ACCOUNT_ACTIVATION_DAYS = 3

EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_HOST_USER = '1a53c2d1df7afd'
EMAIL_HOST_PASSWORD = 'b6903e1447c67a'
EMAIL_PORT = '2525'

PAYPAL_MODE = 'sandbox'
PAYPAL_CLIENT_ID = 'AR3YR2qBpD7U57L54LwRE9JZ2whWzLilT_iBhCk_fZpSsEbFEilIx_WUvhJW81XN92d5Gqa0WXSDg2aj'
PAYPAL_CLIENT_SECRET = 'EP4TagPyKcBBUNBNY12OB_c-saaD6rfY0tpkh155s1cZnZIP1hnjg236Xg08xTFmfk7cLvMr6SOTAQqr'
PAYPAL_CREATE_PRODUCT_URL = 'https://api.sandbox.paypal.com/v1/catalogs/products'
PAYPAL_CREATE_PLAN_URL = 'https://api.sandbox.paypal.com/v1/billing/plans'

RECAPTCHA_PUBLIC_KEY = '6LdJNvIUAAAAAI0QcjHMItzwlPJr75El75cDYVla'
RECAPTCHA_PRIVATE_KEY = '6LdJNvIUAAAAAMSQqxy2tBVXosFk1XIMXtMnMmlp'
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

DJANGO_CSV_GLOBAL_EXPORTS_ENABLED = True
