import pytest
from mixer.backend.django import mixer

from apps.core.models import Setting

pytestmark = pytest.mark.django_db


class TestSetting:
    def test_get_present_attr(self):
        mixer.blend('core.Setting', key='TEST_FOO', value='BAR')

        assert Setting.get('TEST_FOO') == 'BAR'

    def test_get_missing_attr(self):
        assert Setting.get('TEST_FOO') is None
