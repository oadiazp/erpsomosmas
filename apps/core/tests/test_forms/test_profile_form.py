import pytest
from django.contrib.auth.models import User
from mixer.backend.django import mixer

from apps.core.forms import ProfileUpdateForm

pytestmark = pytest.mark.django_db


class TestProfileForm:
    def test_save_incomplete_profile(self):
        user = mixer.blend('auth.User')
        profile = mixer.blend('core.Profile', user=user)

        form = ProfileUpdateForm(
            instance=profile,
            data={
                'first_name': 'Foo',
                'last_name': 'Bar',
                'email': 'foo@bar.com'
            }
        )

        assert not form.is_valid()
