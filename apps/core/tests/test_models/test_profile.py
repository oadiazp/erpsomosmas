from collections import namedtuple

import pytest
from mixer.backend.django import mixer

from apps.core.models import Profile

pytestmark = pytest.mark.django_db


class TestProfile:
    def test_the_profile_is_not_complete(self):
        profile = mixer.blend('core.Profile', phone=None)

        assert not profile.is_complete

    def test_the_profile_is_complete(self):
        user = mixer.blend(
            'auth.User',
            email='a@a.com',
            first_name='F',
            last_name='L'
        )
        profile = mixer.blend(
            'core.Profile',
            user=user,
            phone='123',
            street='AStr.',
            house_number='1A',
            zip_code='10178',
            state='Berlin',
            country='DE',
            city='Berlin'
        )

        assert profile.is_complete

    def test_all_properties_are_defined(self):
        Cls = namedtuple('TestObj', ['foo'])
        obj = Cls(foo=True)

        assert Profile.all_properties_defined(obj, ['foo'])

    def test_not_all_properties_are_defined(self):
        Cls = namedtuple('TestObj', ['foo'])
        obj = Cls(foo=True)

        assert not Profile.all_properties_defined(obj, ['bar'])

    def test_get_paypal_plan(self):
        self._create_paypal_plan_settings()
        mx_profile, us_profile, de_profile = self._create_region_profiles()

        assert mx_profile.paypal_plan == 'LA'
        assert us_profile.paypal_plan == 'US'
        assert de_profile.paypal_plan == 'EU'

    def test_payment_region(self):
        self._create_paypal_plan_settings()
        mx_profile, us_profile, de_profile = self._create_region_profiles()

        assert mx_profile.payment_region == 'LA'
        assert de_profile.payment_region == 'EU'
        assert us_profile.payment_region == 'US'

    def test_has_payments(self):
        payments_profile = mixer.blend('core.Profile')
        mixer.blend('core.Payment', profile=payments_profile)

        wo_payments_profile = mixer.blend('core.Profile')

        assert payments_profile.has_payments
        assert not wo_payments_profile.has_payments

    def _create_region_profiles(self):
        mx_profile = mixer.blend('core.Profile', country='MX')
        us_profile = mixer.blend('core.Profile', country='US')
        de_profile = mixer.blend('core.Profile', country='DE')

        return mx_profile, us_profile, de_profile

    def _create_paypal_plan_settings(self):
        eu_paypaL_setting = mixer.blend('core.Setting', key='PAYPAL_PLAN_EU', value='EU')
        us_paypaL_setting = mixer.blend('core.Setting', key='PAYPAL_PLAN_US', value='US')
        la_paypaL_setting = mixer.blend('core.Setting', key='PAYPAL_PLAN_LA', value='LA')

        return eu_paypaL_setting, us_paypaL_setting, la_paypaL_setting

