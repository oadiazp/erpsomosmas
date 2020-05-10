import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


class TestMassMailCriteria:
    def test_filter_by_countries(self):
        criteria = mixer.blend('core.MassMailCriteria', field='country', value='CU')

        assert criteria.filter_dict == {
            'country': 'CU'
        }
