from django.db import models
from model_utils.models import TimeStampedModel


class Move(TimeStampedModel):
    concept = models.CharField(max_length=200)
    date = models.DateField()
    amount = models.FloatField()
    income = models.BooleanField()
