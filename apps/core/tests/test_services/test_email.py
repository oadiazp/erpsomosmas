from django.core import mail
from django.test import TestCase

from apps.core.emails import Email


class TestEmail(TestCase):
    def test_send(self):
        class EmailTest(Email):
            body_template = 'emails/test.txt'
            subject = 'Test'

        email_test = EmailTest(destinations=['a@a.com'])
        email_test.send()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Test')
        self.assertIn('Test email', mail.outbox[0].body)
