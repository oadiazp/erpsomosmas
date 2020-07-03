import pytest
from mixer.backend.django import mixer

from apps.core.services import PaymentCounter

pytestmark = pytest.mark.django_db


class TestPaymentCounter:
    def test_count(self):
        user = mixer.blend('auth.User', email='foo@test.com')
        profile = mixer.blend('core.Profile', user=user)
        mixer.blend('core.Payment', profile=profile)

        assert PaymentCounter(email='foo@test.com').count == 1