from apps.core.models import Profile
from apps.core.payment_methods import PayPalPaymentMethod


class ReceivePayment:
    def __init__(self, payload):
        self.payload = payload

    def execute(self, paypal_mode, paypal_client_id, paypal_secret_id):
        payment = PayPalPaymentMethod.get_payment(
            self.payload['resource']['parent_payment'],
            paypal_mode,
            paypal_client_id,
            paypal_secret_id
        )
        payer_email = payment['payer']['payer_info']['email']

        profile = Profile.objects.filter(paypal_email=payer_email)

        if profile:
            profile = profile.first()

        profile.add_payment(
            amount=payment['transactions'][0]['amount']['total']
        )
