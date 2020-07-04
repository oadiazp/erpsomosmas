import pytest
from django.contrib.auth.models import User

from apps.core.models import Profile
from apps.core.services import FakeProfileCreator

pytestmark = pytest.mark.django_db


class TestFakeProfileCreator:
    def test_creation(self):
        payload = {
            "id": "I-1TJ3GAGG82Y9",
            "state": "Active",
            "description": "Monthly agreement with free trial payment definition.",
            "payer": {
                "payment_method": "paypal",
                "status": "unverified",
                "payer_info": {
                    "email": "johndoe@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "payer_id": "NEW8A85AK4ET4",
                    "shipping_address": {
                        "recipient_name": "John Doe",
                        "line1": "751235 Stout Drive",
                        "line2": "0976249 Elizabeth Court",
                        "city": "Quimby",
                        "state": "IA",
                        "postal_code": "51049",
                        "country_code": "US"
                    }
                }
            },
            "plan": {
                "name": "Plan with Regular and Trial Payment Definitions",
                "description": "Plan with regular and trial payment definitions.",
                "type": "FIXED",
                "payment_definitions": [
                    {
                        "name": "Trial payment definition",
                        "type": "TRIAL",
                        "frequency": "MONTH",
                        "amount": {
                            "value": "0.00",
                            "currency": "USD"
                        },
                        "cycles": "2",
                        "charge_models": [
                            {
                                "type": "TAX",
                                "amount": {
                                    "value": "0.00",
                                    "currency": "USD"
                                }
                            },
                            {
                                "type": "SHIPPING",
                                "amount": {
                                    "value": "0.00",
                                    "currency": "USD"
                                }
                            }
                        ],
                        "frequency_interval": "1"
                    },
                    {
                        "name": "Regular payment definition",
                        "type": "REGULAR",
                        "frequency": "MONTH",
                        "amount": {
                            "value": "5.99",
                            "currency": "USD"
                        },
                        "cycles": "10",
                        "charge_models": [
                            {
                                "type": "TAX",
                                "amount": {
                                    "value": "0.29",
                                    "currency": "USD"
                                }
                            },
                            {
                                "type": "SHIPPING",
                                "amount": {
                                    "value": "0.20",
                                    "currency": "USD"
                                }
                            }
                        ],
                        "frequency_interval": "1"
                    }
                ],
                "merchant_preferences": {
                    "setup_fee": {
                        "value": "0.40",
                        "currency": "USD"
                    },
                    "return_url": "https://example.com",
                    "cancel_url": "https://example.com/cancel",
                    "max_fail_attempts": "2",
                    "auto_bill_amount": "YES"
                },
                "links": [],
                "currency_code": "USD"
            },
            "start_date": "2016-12-23T08:00:00Z",
            "shipping_address": {
                "recipient_name": "John Doe",
                "line1": "751235 Stout Drive",
                "line2": "0976249 Elizabeth Court",
                "city": "Quimby",
                "state": "IA",
                "postal_code": "51049",
                "country_code": "US"
            },
            "agreement_details": {
                "outstanding_balance": {
                    "currency": "USD",
                    "value": "0.00"
                },
                "cycles_remaining": "2",
                "cycles_completed": "0",
                "next_billing_date": "2017-01-23T08:00:00Z",
                "last_payment_date": "2016-12-23T08:00:00Z",
                "last_payment_amount": {
                    "currency": "USD",
                    "value": "0.40"
                },
                "final_payment_date": "2017-09-23T08:00:00Z",
                "failed_payment_count": "0"
            },
            "links": [
                {
                    "href": "https://api.sandbox.paypal.com/v1/payments/billing-agreements/I-1TJ3GAGG82Y9/suspend",
                    "rel": "suspend",
                    "method": "POST"
                },
                {
                    "href": "https://api.sandbox.paypal.com/v1/payments/billing-agreements/I-1TJ3GAGG82Y9/re-activate",
                    "rel": "re_activate",
                    "method": "POST"
                },
                {
                    "href": "https://api.sandbox.paypal.com/v1/payments/billing-agreements/I-1TJ3GAGG82Y9/cancel",
                    "rel": "cancel",
                    "method": "POST"
                },
                {
                    "href": "https://api.sandbox.paypal.com/v1/payments/billing-agreements/I-1TJ3GAGG82Y9/bill-balance",
                    "rel": "self",
                    "method": "POST"
                },
                {
                    "href": "https://api.sandbox.paypal.com/v1/payments/billing-agreements/I-1TJ3GAGG82Y9/set-balance",
                    "rel": "self",
                    "method": "POST"
                }
            ]
        }

        profile = FakeProfileCreator(payload).create()

        user = profile.user
        assert user.first_name == 'John'
        assert user.last_name == 'Doe'
        assert user.is_active is True

        assert profile.street == '751235 Stout Drive'
        assert profile.zip_code == '51049'
        assert profile.state == 'IA'
        assert profile.country == 'US'
        assert profile.paypal_email == 'johndoe@example.com'