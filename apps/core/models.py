import pytest
from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField

from model_utils.models import TimeStampedModel


class Profile(TimeStampedModel):
    phone = models.CharField(max_length=20)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=5)
    zip_code = models.IntegerField()
    state = models.CharField(max_length=100)
    country = CountryField()

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        if self.user:
            return f'{self.user.first_name} {self.user.last_name}'
        else:
            return ''
