from unittest.mock import patch

import pytest
from mixer.backend.django import mixer

from apps.core.models import Payment
from apps.core.services import ReceivePayment

pytestmark = pytest.mark.django_db


class TestReceivePayment:
    def test_profile_is_updated_after_a_successful_payment(self):
        profile = mixer.blend('core.Profile', paypal_email='foo@paypal.com')

        receive_payment_service = ReceivePayment({
            'resource': {
                'id': 'TestID',
                'billing_agreement_id': 123,
                'amount': {
                    'total': 10
                }
            }
        })
        with patch('apps.core.payment_methods.PayPalPaymentMethod.get_billing_agreement') as mock:
            mock.return_value = {
                'id': 'TestID',
                'payer': {
                    'payer_info': {
                        'email': 'foo@paypal.com'
                    },
                }
            }
            receive_payment_service.execute(
                'sandbox',
                'test_client_id',
                'test_secret_id'
            )

        payment = Payment.objects.filter(profile=profile)

        if payment:
            payment = payment.first()

        assert payment.amount == 10
        assert payment.reference == 'TestID'
