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
                'parent_payment': 123
            }
        })
        with patch('apps.core.payment_methods.PayPalPaymentMethod.get_payment') as mock:
            mock.return_value = {
                'payer': {
                    'payer_info': {
                        'email': 'foo@paypal.com'
                    }
                },
                'transactions': [
                    {
                        'amount': {
                            'total': 10
                        }
                    }
                ]
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
