from django.db import models

class PackageType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Package(models.Model):
    name = models.CharField(max_length=255)
    weight = models.FloatField()
    price = models.PositiveIntegerField()
    package_type = models.ForeignKey(models, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
