import pytest
from mixer.backend.django import mixer

from apps.reports.services import Members

pytestmark = pytest.mark.django_db


class TestMembers:
    def test_amount_by_continent(self):
        us = mixer.blend('core.Profile', country='US')
        mixer.blend('core.Payment', profile=us)
        ca = mixer.blend('core.Profile', country='CA')
        mixer.blend('core.Payment', profile=ca)
        mx = mixer.blend('core.Profile', country='MX')
        mixer.blend('core.Payment', profile=mx)
        au = mixer.blend('core.Profile', country='AU')
        mixer.blend('core.Payment', profile=au)

        assert Members.get_members_amount_by_continent('North America') == 3

    def test_get_countries_by_continent(self):
        assert 'MX' in Members.get_countries_by_continent('North America')
        assert 'CA' in Members.get_countries_by_continent('North America')
        assert 'US' in Members.get_countries_by_continent('North America')
