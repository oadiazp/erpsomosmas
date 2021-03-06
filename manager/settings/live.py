from apps.utils import get_secret
from .base import *
from datetime import timedelta
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


MEDIA_URL = get_secret('MEDIA_URL')
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_S3_REGION_NAME = get_secret('AWS_REGION')
AWS_S3_BUCKET_AUTH = False
AWS_S3_MAX_AGE_SECONDS = int(timedelta(days=7).total_seconds())
AWS_STORAGE_BUCKET_NAME = 'somosmas-management'
AWS_ACCESS_KEY_ID = get_secret('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_secret('ERP_AWS_SECRET_ACCESS_KEY')
AWS_S3_SIGNATURE_VERSION = 's3v4'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': get_secret('DB_HOST'),
        'USER': get_secret('DB_USER'),
        'PASSWORD': get_secret('ERP_DB_PASSWORD'),
        'NAME': get_secret('DB_NAME'),
        'ATOMIC_REQUESTS': True,
    }
}

DEBUG = False

EMAIL_HOST_PASSWORD = get_secret('ERP_EMAIL_HOST_PASSWORD')
EMAIL_HOST = get_secret('EMAIL_HOST')
EMAIL_HOST_USER = get_secret('EMAIL_HOST_USER')
EMAIL_PORT = get_secret('EMAIL_PORT')
REGISTRATION_DEFAULT_FROM_EMAIL = get_secret('REGISTRATION_DEFAULT_FROM_EMAIL')

PAYPAL_CLIENT_SECRET = get_secret('ERP_PAYPAL_CLIENT_SECRET')
PAYPAL_MODE = get_secret('PAYPAL_MODE')
PAYPAL_CLIENT_ID = get_secret('PAYPAL_CLIENT_ID')
PAYPAL_CREATE_PRODUCT_URL = get_secret('PAYPAL_CREATE_PRODUCT_URL')
PAYPAL_CREATE_PLAN_URL = get_secret('PAYPAL_CREATE_PLAN_URL')
AWS_DEFAULT_ACL = 'public-read'

sentry_sdk.init(
    dsn="https://d653e0ec680640a6b0a2f52f3259b1a4@sentry.zczoft.com/3",
    integrations=[DjangoIntegration()]
)

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

DEFAULT_FROM_EMAIL = 'tecnologia@somosmascuba.com'
SENDGRID_API_KEY = get_secret('ERP_SENDGRID_API_KEY')

EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'

RECAPTCHA_PUBLIC_KEY = get_secret('ERP_RECAPTCHA_PUBLIC_KEY', 'fake')
RECAPTCHA_PRIVATE_KEY = get_secret('ERP_RECAPTCHA_PRIVATE_KEY', 'fake')
SILENCED_SYSTEM_CHECKS = []


CKEDITOR_BASEPATH = '/ckeditor/ckeditor'
AWS_QUERYSTRING_AUTH = False
