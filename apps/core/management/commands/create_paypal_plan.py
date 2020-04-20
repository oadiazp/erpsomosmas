from django.conf import settings
from django.core.management import BaseCommand

from apps.core.models import Setting
from apps.core.payment_methods import PayPalPaymentMethod


class Command(BaseCommand):
    help = 'Create a PayPal plan'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str)
        parser.add_argument('price', type=int)

    def handle(self, *args, **options):
        access_token = PayPalPaymentMethod.access_token(
            settings.PAYPAL_MODE,
            settings.PAYPAL_CLIENT_ID,
            settings.PAYPAL_CLIENT_SECRET,
        )
        product_id = PayPalPaymentMethod.create_product(
            settings.PAYPAL_CREATE_PRODUCT_URL,
            options['name'],
            access_token
        )
        plan_id = PayPalPaymentMethod.create_plan(
            settings.PAYPAL_CREATE_PLAN_URL,
            access_token,
            product_id,
            options['price']
        )

        setting = Setting.objects.create(
            key=f'PAYPAL_PRODUCT_{options["name"].upper()}',
            value=plan_id
        )

        print(setting)
