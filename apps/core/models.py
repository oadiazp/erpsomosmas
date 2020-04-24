from json import dumps

from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField
from geonamescache import GeonamesCache

from model_utils.models import TimeStampedModel


class PaymentMethod(TimeStampedModel):
    name = models.CharField(max_length=20)
    icon = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Profile(TimeStampedModel):
    phone = models.CharField(max_length=20, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    house_number = models.CharField(max_length=5, null=True, blank=True)
    zip_code = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = CountryField(null=True, blank=True)
    paypal_email = models.EmailField(blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )

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

    @property
    def paypal_plan(self):
        gc = GeonamesCache()
        continent = gc.get_countries()[self.country]['continentcode']

        if continent == 'EU':
            return Setting.get('PAYPAL_PLAN_EU')
        elif continent[-1] == 'A' and self.country not in ['US', 'CA']:
            return Setting.get('PAYPAL_PLAN_LA')

        return Setting.get('PAYPAL_PLAN_US')

    def add_payment(self, amount):
        Payment.objects.create(profile=self, amount=amount)


class Payment(TimeStampedModel):
    amount = models.FloatField()

    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)


class Setting(TimeStampedModel):
    key = models.CharField(max_length=200, unique=True)
    value = models.CharField(max_length=200)

    def __str__(self):
        return dumps({
            self.key: self.value
        })

    @staticmethod
    def get(item, default=None):
        setting = Setting.objects.filter(key=item)

        if setting:
            return setting.first().value

        return default


from .signals import *  # noqa
