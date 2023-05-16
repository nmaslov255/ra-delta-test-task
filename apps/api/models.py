from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.sessions.models import Session
from apps.settings import (
    MAX_USD_RUB_EXCHANGE_RATE,
    MAX_PACKAGE_WEIGHT,
    MAX_PACKAGE_PRICE
)

from .validators import raise_for_invalide_name
from .utils import calculate_delivery_price

MAX_DELIVERY_PRICE = calculate_delivery_price(
    MAX_PACKAGE_WEIGHT, MAX_PACKAGE_PRICE, MAX_USD_RUB_EXCHANGE_RATE
)


class PackageType(models.Model):
    name = models.CharField(
        max_length=255, validators=[raise_for_invalide_name]
    )

    def __str__(self):
        return self.name


class Package(models.Model):
    name = models.CharField(
        max_length=255, validators=[raise_for_invalide_name]
    )

    weight = models.FloatField(validators=[
        MinValueValidator(0.1), MaxValueValidator(MAX_PACKAGE_WEIGHT)
    ])

    price = models.PositiveIntegerField(validators=[
        MinValueValidator(1), MaxValueValidator(MAX_PACKAGE_PRICE)
    ])

    delivery_price = models.PositiveIntegerField(validators=[
        MinValueValidator(1), MaxValueValidator(MAX_DELIVERY_PRICE)
    ], null=True, default=None)

    package_type = models.ForeignKey(PackageType, on_delete=models.PROTECT)
    owner_session = models.ForeignKey(Session, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
