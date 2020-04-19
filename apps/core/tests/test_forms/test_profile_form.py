import pytest
from django.contrib.auth.models import User
from mixer.backend.django import mixer

from apps.core.forms import ProfileUpdateForm
from apps.core.models import Profile

pytestmark = pytest.mark.django_db


class TestProfileForm:
    def test_save_user_attrs(self):
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

        form.is_valid()
        form.save(True)

        user = User.objects.first()
        assert user.first_name == 'Foo'
        assert user.last_name == 'Bar'
        assert user.email == 'foo@bar.com'
