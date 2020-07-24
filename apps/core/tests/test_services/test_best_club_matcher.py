import pytest
from mixer.backend.django import mixer

from apps.core.services import BestClubMatcher

pytestmark = pytest.mark.django_db


class TestBestClubMatcher:
    def test_find_best_match_with_several_clubs(self):
        es_club = mixer.blend(
            'core.Club',
            coordinator=mixer.blend('core.Profile')
        )
        madrid_club = mixer.blend(
            'core.Club',
            coordinator=mixer.blend('core.Profile')
        )
        rivas_club = mixer.blend(
            'core.Club',
            coordinator=mixer.blend('core.Profile')
        )

        es_criteria = mixer.blend('core.Criteria', field='country', value='ES')
        madrid_criteria = mixer.blend(
            'core.Criteria',
            field='city',
            value='Madrid'
        )
        rivas_criteria = mixer.blend(
            'core.Criteria',
            field='zip_code__in',
            value='["2222","2223"]'
        )

        es_club.criterias.add(es_criteria)

        madrid_club.criterias.add(es_criteria)
        madrid_club.criterias.add(madrid_criteria)

        rivas_club.criterias.add(es_criteria)
        rivas_club.criterias.add(madrid_criteria)
        rivas_club.criterias.add(rivas_criteria)

        es_profile = mixer.blend('core.Profile', country='ES')
        madrid_profile = mixer.blend('core.Profile', country='ES',
                                     city='Madrid')
        rivas_profile = mixer.blend('core.Profile', country='ES', city='Madrid',
                                    zip_code='2222')

        assert BestClubMatcher.find(es_profile) == es_club
        assert BestClubMatcher.find(madrid_profile) == madrid_club
        assert BestClubMatcher.find(rivas_profile) == rivas_club

        assert es_profile in es_club.members.all()
        assert madrid_profile in madrid_club.members.all()
        assert rivas_profile in rivas_club.members.all()
