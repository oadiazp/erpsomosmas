from json import dumps

from paypalrestsdk import Api, Webhook, Payment, Order, BillingAgreement
from requests import post


class PayPalPaymentMethod:

    @staticmethod
    def access_token(mode, client_id, client_secret):
        api = Api({
            'mode': mode,
            'client_id': client_id,
            'client_secret': client_secret
        })

        return api.get_access_token()

    @staticmethod
    def create_product(url, name, token):
        return post(
            url,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            },
            data=dumps({
                'name': name,
                'description': "S+'s membership",
                'type': 'SERVICE',
                'image_url': 'https://somosmascuba.com/wp-content/uploads/2016/01/header20164.jpg',
                'home_url': 'https://somosmascuba.com'
            })
        ).json()['id']

    @staticmethod
    def create_plan(url, token, product_id, price):
        return post(
            url,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            },
            data=dumps({
                "product_id": product_id,
                "name": "Basic Plan",
                "description": "Basic plan",
                "billing_cycles": [
                    {
                        "frequency": {
                            "interval_unit": "MONTH",
                            "interval_count": 1
                        },
                        "tenure_type": "REGULAR",
                        "sequence": 1,
                        "pricing_scheme": {
                            "fixed_price": {
                                "value": str(price),
                                "currency_code": "USD"
                            }
                        }
                    }
                ],
                "payment_preferences": {
                    "auto_bill_outstanding": True,
                    "setup_fee_failure_action": "CONTINUE",
                    "payment_failure_threshold": 3
                },
                "taxes": {
                    "percentage": "3",
                    "inclusive": 1
                }
            })
        ).json()['id']

    @staticmethod
    def create_webhook(events, url, mode, client_id, client_secret):
        webhook = Webhook(
            {
                'url': url,
                'event_types': [
                    {'name': event} for event in events
                ]
            },
            api=Api({
                'mode': mode,
                'client_id': client_id,
                'client_secret': client_secret
            })
        )

        if webhook.create():
            print("Webhook[%s] created successfully" % (webhook.id))
        else:
            print(webhook.error)

    @staticmethod
    def get_payment(payment_id, paypal_mode, paypal_client_id,
                    paypal_client_secret):
        return Payment.find(
            resource_id=payment_id,
            api=Api({
                'mode': paypal_mode,
                'client_id': paypal_client_id,
                'client_secret': paypal_client_secret
            })
        )

    @staticmethod
    def get_billing_agreement(
        billing_agreement_id,
        paypal_mode,
        paypal_client_id,
        paypal_client_secret
    ):
        return BillingAgreement.find(
            billing_agreement_id,
            api=Api({
                'mode': paypal_mode,
                'client_id': paypal_client_id,
                'client_secret': paypal_client_secret
            })
        )

    @staticmethod
    def get_order(
            order_id,
            paypal_mode,
            paypal_client_id,
            paypal_client_secret
    ):
        return Order.find(
            resource_id=order_id,
            api=Api({
                'mode': paypal_mode,
                'client_id': paypal_client_id,
                'client_secret': paypal_client_secret
            })
        )
