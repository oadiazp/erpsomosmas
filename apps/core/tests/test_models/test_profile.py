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
            country='DE'
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
