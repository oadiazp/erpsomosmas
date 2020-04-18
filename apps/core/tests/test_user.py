import pytest
from mixer.backend.django import mixer

from apps.core.models import Profile

pytestmark = pytest.mark.django_db


class TestUser:
    def test_a_profile_is_created_when_an_user_is_created(self):
        mixer.blend('auth.User')

        assert Profile.objects.count() == 1
