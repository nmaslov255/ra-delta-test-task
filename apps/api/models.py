from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from .form import validate_name


class PackageType(models.Model):
    name = models.CharField(max_length=255, validators=[validate_name])

    def __str__(self):
        return self.name

class Package(models.Model):
    name = models.CharField(max_length=255, validators=[validate_name])
    weight = models.FloatField(validators=[MinValueValidator(0.1),
                                           MaxValueValidator(1000)])
    price = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    package_type = models.ForeignKey(PackageType, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
