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


from .signals import  *  # noqa