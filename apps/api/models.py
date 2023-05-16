from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.sessions.models import Session

from .validators import raise_for_invalide_name


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

    weight = models.FloatField(
        validators=[MinValueValidator(0.1), MaxValueValidator(1000)]
    )

    price = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000000)]
    )
    delivery_price = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000000000)],
        null=True, default=None
    )

    package_type = models.ForeignKey(PackageType, on_delete=models.PROTECT)
    owner_session = models.ForeignKey(Session, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
