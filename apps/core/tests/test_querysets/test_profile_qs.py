import pytest
from mixer.backend.django import mixer

from apps.core.models import Profile

pytestmark = pytest.mark.django_db


class TestProfileQS:
    def test_members_amount(self):
        profile = mixer.blend('core.Profile', country='US')

        for _ in range(0, 10):
            mixer.blend('core.Payment', profile=profile)

        assert Profile.objects.members().count() == 1
