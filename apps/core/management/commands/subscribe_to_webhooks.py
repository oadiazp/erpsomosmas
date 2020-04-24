from django.conf import settings
from django.core.management import BaseCommand

from apps.core.models import Setting
from apps.core.payment_methods import PayPalPaymentMethod


class Command(BaseCommand):
    help = 'Subscribe to a PayPal webhook'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str)
        parser.add_argument('events', type=str, nargs='+')

    def handle(self, *args, **options):
        PayPalPaymentMethod.create_webhook(
            options['events'],
            options['url'],
            settings.PAYPAL_MODE,
            settings.PAYPAL_CLIENT_ID,
            settings.PAYPAL_CLIENT_SECRET
        )
