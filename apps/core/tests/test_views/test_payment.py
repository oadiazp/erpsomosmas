import pytest
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory
from mixer.backend.django import mixer

from apps.core.views import PaymentView

pytestmark = pytest.mark.django_db


class TestPaymentView:
    def test_anonymous(self):
        request = RequestFactory().get('/payment')
        request.user = AnonymousUser()
        response = PaymentView.as_view()(request)

        assert response.status_code == 302
        assert 'login' in response.url

    def test_authenticated_wo_payments(self):
        request = RequestFactory().get('/payment')
        request.user = User()
        response = PaymentView.as_view()(request)

        assert response.status_code == 200
        response.render()
        assert 'S+' in response.content.decode('utf-8')

    def test_authenticated_with_payments(self):
        profile = mixer.blend('core.Profile')
        mixer.blend('core.Payment', profile=profile)

        request = RequestFactory().get('/payment')
        request.user = profile.user

        response = PaymentView.as_view()(request)

        assert response.status_code == 302
        assert 'general' in response.url
