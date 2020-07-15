import pytest
from django.test import TestCase
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


class TestMassMail(TestCase):
    def test_profiles_filtered_by_profiles_attrs(self):
        cuban_profile = mixer.blend('core.Profile', country='CU')
        us_profile = mixer.blend('core.Profile', country='US')
        mx_profile = mixer.blend('core.Profile', country='MX')

        mass_mail = mixer.blend('core.MassMail')
        criteria = mixer.blend(
            'core.Criteria',
            mass_mail=mass_mail,
            field='country__in',
            value="['CU','US']"
        )
        mass_mail.criterias.add(criteria)

        assert cuban_profile in mass_mail.recipients
        assert us_profile in mass_mail.recipients
        assert mx_profile not in mass_mail.recipients

    def test_filter_missing_first_name(self):
        cuban_profile = mixer.blend(
            'core.Profile',
            country='CU',
            user=mixer.blend('auth.User', first_name='Foo')
        )
        us_profile = mixer.blend(
            'core.Profile',
            country='US',
            user=mixer.blend('auth.User', first_name='')
        )

        mass_mail = mixer.blend('core.MassMail')
        criteria = mixer.blend(
            'core.Criteria',
            mass_mail=mass_mail,
            field='user__first_name',
            value=""
        )
        mass_mail.criterias.add(criteria)

        assert cuban_profile not in mass_mail.recipients
        assert us_profile in mass_mail.recipients

    def test_filter_missing_payments(self):
        cuban_profile = mixer.blend(
            'core.Profile',
            country='CU',
        )
        us_profile = mixer.blend(
            'core.Profile',
            country='US',
        )
        mixer.blend('core.Payment', profile=us_profile)

        mass_mail = mixer.blend('core.MassMail')
        criteria = mixer.blend(
            'core.Criteria',
            mass_mail=mass_mail,
            field='payment__isnull',
            value="1"
        )

        mass_mail.criterias.add(criteria)

        assert us_profile not in mass_mail.recipients
        assert cuban_profile in mass_mail.recipients

    def test_filter_inactive(self):
        cuban_profile = mixer.blend(
            'core.Profile',
            country='CU',
            user=mixer.blend('auth.User', is_active=True)
        )
        us_profile = mixer.blend(
            'core.Profile',
            country='US',
            user=mixer.blend('auth.User', is_active=False)
        )

        mass_mail = mixer.blend('core.MassMail')
        criteria = mixer.blend(
            'core.Criteria',
            field='user__is_active',
            value="1"
        )
        mass_mail.criterias.add(criteria)

        assert us_profile not in mass_mail.recipients
        assert cuban_profile in mass_mail.recipients
