from json import dumps

from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField
from geonamescache import GeonamesCache

from model_utils.models import TimeStampedModel

from .querysets import ProfileQS


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
    paypal_email = models.EmailField(null=True, blank=True)
    photo = models.FileField(upload_to='photos/', null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    objects = ProfileQS.as_manager()

    def __str__(self):
        if self.user:
            return f'{self.user.first_name} {self.user.last_name}'
        else:
            return ''

    @classmethod
    def all_properties_defined(cls, obj, attrs):
        return all(
            [
                hasattr(obj, attr) and getattr(obj, attr) is not None for attr in attrs
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
        return Setting.get(f'PAYPAL_PLAN_{self.payment_region}')

    def add_payment(self, amount, reference):
        Payment.objects.create(profile=self, amount=amount, reference=reference)

    @property
    def payment_region(self):
        gc = GeonamesCache()
        continent = gc.get_countries()[self.country]['continentcode']

        if continent == 'EU':
            return 'EU'
        elif continent[-1] == 'A' and self.country not in ['US', 'CA']:
            return 'LA'

        return 'US'

    @property
    def membership_price(self):
        setting = Setting.objects.filter(
            key=f'PAYPAL_MEMBERSHIP_PRICE_{ self.payment_region }'
        )

        if setting:
            setting = setting.first()

            return float(setting.value)

        return 0


class Payment(TimeStampedModel):
    amount = models.FloatField()
    reference = models.CharField(max_length=200)

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


class Expense(TimeStampedModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    amount = models.FloatField()
    fixed = models.BooleanField()


class Donation(TimeStampedModel):
    name = models.CharField(max_length=200)
    reference = models.CharField(max_length=200)
    payer = models.EmailField()
    amount = models.FloatField()

from .signals import *  # noqa
