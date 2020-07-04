from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext as _


class Email:
    body_template = None
    subject = None
    destinations = []

    def __init__(self, destinations):
        self.destinations = destinations

    def send(self):
        send_mail(
            subject=self.subject,
            message=render_to_string(
                template_name=self.body_template,
                context=self.get_context(),
            ),
            recipient_list=self.get_destinations(),
            from_email=settings.DEFAULT_FROM_EMAIL
        )

    def get_destinations(self):
        return self.destinations

    def get_context(self):
        return {}


class WelcomeEmail(Email):
    body_template = 'emails/welcome.txt'
    subject = _('[ERP S+] Welcome')


class PaymentConfirmationEmail(Email):
    body_template = 'emails/payment_confirmation.txt'
    subject = _('[ERP S+] Payment confirmation')
