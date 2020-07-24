from django.contrib.auth.models import User
from django.db.models import Count
from apps.core.models import Profile, Payment, Club

from apps.core.payment_methods import PayPalPaymentMethod


class ReceivePayment:
    def __init__(self, payload):
        self.payload = payload
        self.email = None

    def execute(self, paypal_mode, paypal_client_id, paypal_secret_id):
        billing_agreement = PayPalPaymentMethod.get_billing_agreement(
            self.payload['resource']['billing_agreement_id'],
            paypal_mode,
            paypal_client_id,
            paypal_secret_id
        )
        payer_email = billing_agreement['payer']['payer_info']['email']
        self.email = payer_email

        profile = Profile.objects.filter(paypal_email=payer_email)

        if profile:
            profile = profile.first()
        else:
            profile = FakeProfileCreator(billing_agreement).create()

        profile.add_payment(
            amount=self.payload['resource']['amount']['total'],
            reference=self.payload['resource']['id']
        )


class PaymentCounter:
    def __init__(self, email):
        self.email = email

    @property
    def amount(self):
        return Payment.objects.filter(profile__user__email=self.email).count()


class FakeProfileCreator:
    def __init__(self, billing_agreement):
        self.billing_agreement = billing_agreement

    def create(self):
        user = User.objects.create(
            first_name=(
                self.billing_agreement['payer']['payer_info']['first_name']
            ),
            last_name=(
                self.billing_agreement['payer']['payer_info']['last_name']
            ),
            is_active=True,
            username=self.billing_agreement['payer']['payer_info']['email'],
        )

        profile = Profile.objects.filter(user=user).first()
        address = (
            self.billing_agreement['payer']['payer_info']['shipping_address']
        )

        profile.street = address['line1']
        profile.zip_code = address['postal_code']
        profile.state = address['state']
        profile.country = address['country_code']
        profile.paypal_email = (
            self.billing_agreement['payer']['payer_info']['email']
        )
        profile.save()

        return profile


class BestClubMatcher:
    @staticmethod
    def find(profile):
        sorted_clubs = Club.objects.all().annotate(
            amount=Count('criterias')
        ).order_by('-amount')

        for club in sorted_clubs:
            if club.match(profile):
                return club
