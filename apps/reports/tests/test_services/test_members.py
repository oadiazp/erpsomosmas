import pytest
from mixer.backend.django import mixer

from apps.reports.services import Members

pytestmark = pytest.mark.django_db


class TestMembers:
    def test_get_countries_by_continent(self):
        assert 'MX' in Members.get_countries_by_continent('North America')
        assert 'CA' in Members.get_countries_by_continent('North America')
        assert 'US' in Members.get_countries_by_continent('North America')
