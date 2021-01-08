from unittest.mock import patch

import pytest
from django.contrib.auth.models import User
from mixer.backend.django import mixer

from apps.core.models import Profile, Payment
from apps.core.services import UserRemoval

pytestmark = pytest.mark.django_db


class TestUserRemoval:
    def test_remove(self):
        user = mixer.blend('auth.User', username='test')
        profile = Profile.objects.first()

        mixer.blend('registration.RegistrationProfile', user=user)
        mixer.blend('core.Payment', profile=profile)

        with patch(
            'apps.core.services.UserRemoval.cancel_paypal_billing_agreement'
        ) as mock:
            mock.return_value = None

            UserRemoval.remove(user)

        assert User.objects.count() == 0
        assert Profile.objects.count() == 0
        assert Payment.objects.count() == 0
