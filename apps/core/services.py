from apps.core.models import Profile
from apps.core.payment_methods import PayPalPaymentMethod


class ReceivePayment:
    def __init__(self, payload):
        self.payload = payload

    def execute(self, paypal_mode, paypal_client_id, paypal_secret_id):
        billing_agreement = PayPalPaymentMethod.get_billing_agreement(
            self.payload['resource']['billing_agreement_id'],
            paypal_mode,
            paypal_client_id,
            paypal_secret_id
        )
        payer_email = billing_agreement['payer']['payer_info']['email']

        profile = Profile.objects.filter(paypal_email=payer_email)

        if profile:
            profile = profile.first()

        profile.add_payment(
            amount=self.payload['resource']['amount']['total'],
            reference=self.payload['resource']['id']
        )
