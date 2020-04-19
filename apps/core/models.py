import pytest
from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField

from model_utils.models import TimeStampedModel


class Profile(TimeStampedModel):
    phone = models.CharField(max_length=20, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    house_number = models.CharField(max_length=5, null=True, blank=True)
    zip_code = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = CountryField(null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        if self.user:
            return f'{self.user.first_name} {self.user.last_name}'
        else:
            return ''

    @classmethod
    def all_properties_defined(cls, obj, attrs):
        return all(
            [
                hasattr(obj, attr) and getattr(obj, attr) for attr in attrs
            ]
        )

    @property
    def is_complete(self):
        profile_attrs = [
            'phone',
            'street',
            'house_number',
            'zip_code',
            'state',
            'country'
        ]

        all_profile_props_are_defined = self.all_properties_defined(
            self,
            profile_attrs
        )

        user_attrs = [
            'email',
            'first_name',
            'last_name',
        ]

        all_user_props_are_defined = self.all_properties_defined(
            self.user,
            user_attrs
        )

        return all([all_profile_props_are_defined, all_user_props_are_defined])


from .signals import *  # noqa
