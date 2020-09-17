from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext as _


class Email:
    body_template = None
    subject = None
    destinations = []
    context = {}

    def __init__(self, destinations, context=dict()):
        self.destinations = destinations
        self.context = context

    def send(self):
        context = self.context or self.get_context()

        send_mail(
            subject=self.subject,
            message=render_to_string(
                template_name=self.body_template,
                context=context
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


class WelcomeToClubEmail(Email):
    body_template = 'emails/welcome_to_club.txt'
    subject = _('[ERP S+] Welcome to the club')


class NewClubMemberEmail(Email):
    body_template = 'emails/new_club_member.txt'
    subject = _('[ERP S+] New member to your club')
