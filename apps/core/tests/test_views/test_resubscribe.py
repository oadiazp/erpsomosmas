import pytest
from django.test import RequestFactory
from mixer.backend.django import mixer

from apps.core.views import ResubscribeView

pytestmark = pytest.mark.django_db


class TestResubscribe:
    def test_auth_resubscribe_with_payments(self):
        profile = mixer.blend('core.Profile')
        mixer.blend('core.Payment', profile=profile)

        request = RequestFactory().get('/payment')
        request.user = profile.user

        response = ResubscribeView.as_view()(request)

        assert response.status_code == 200
        response.render()
        assert 'button_paypal' in response.content.decode('utf-8')
