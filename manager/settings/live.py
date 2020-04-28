from apps.utils import get_secret
from .base import *
from datetime import timedelta

MEDIA_URL = get_secret('MEDIA_URL')
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_S3_REGION_NAME = get_secret('AWS_REGION')
AWS_S3_BUCKET_AUTH = False
AWS_S3_MAX_AGE_SECONDS = int(timedelta(days=7).total_seconds())
AWS_STORAGE_BUCKET_NAME = get_secret('AWS_S3_BUCKET_NAME')
AWS_ACCESS_KEY_ID = get_secret('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_secret('AWS_SECRET_ACCESS_KEY')
AWS_S3_SIGNATURE_VERSION = 's3'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': get_secret('DB_HOST'),
        'USER': get_secret('DB_USER'),
        'PASSWORD': get_secret('DB_PASSWORD'),
        'NAME': get_secret('DB_NAME'),
        'ATOMIC_REQUESTS': True,
    }
}

DEBUG = False

EMAIL_HOST_PASSWORD = get_secret('EMAIL_HOST_PASSWORD')
EMAIL_HOST = get_secret('EMAIL_HOST')
EMAIL_HOST_USER = get_secret('EMAIL_HOST_USER')

PAYPAL_CLIENT_SECRET = get_secret('PAYPAL_CLIENT_SECRET')
PAYPAL_MODE = get_secret('PAYPAL_MODE')
PAYPAL_CLIENT_ID = get_secret('PAYPAL_CLIENT_ID')
PAYPAL_CREATE_PRODUCT_URL = get_secret('PAYPAL_CREATE_PRODUCT_URL')
PAYPAL_CREATE_PLAN_URL = get_secret('PAYPAL_CREATE_PLAN_URL')
