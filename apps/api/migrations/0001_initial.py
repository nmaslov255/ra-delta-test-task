# Generated by Django 4.2.1 on 2023-05-16 09:46
# Attention! the maximum values of validators are added manually

import api.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion

from apps.settings import (
    MAX_USD_RUB_EXCHANGE_RATE,
    MAX_PACKAGE_WEIGHT,
    MAX_PACKAGE_PRICE
)

from api.utils import calculate_delivery_price

MAX_DELIVERY_PRICE = calculate_delivery_price(
    MAX_PACKAGE_WEIGHT, MAX_PACKAGE_PRICE, MAX_USD_RUB_EXCHANGE_RATE
)


def add_default_package_type(apps, schema_editor):
    PackageType = apps.get_model("api", "PackageType")

    PackageType.objects.get_or_create(name='Other')
    PackageType.objects.get_or_create(name='Electronics')
    PackageType.objects.get_or_create(name='Clothing')


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sessions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PackageType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, validators=[api.validators.raise_for_invalide_name])),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, validators=[api.validators.raise_for_invalide_name])),
                ('weight', models.FloatField(validators=[django.core.validators.MinValueValidator(0.1), django.core.validators.MaxValueValidator(MAX_PACKAGE_WEIGHT)])),
                ('price', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(MAX_PACKAGE_PRICE)])),
                ('delivery_price', models.PositiveIntegerField(default=None, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(MAX_DELIVERY_PRICE)])),
                ('owner_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sessions.session')),
                ('package_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.packagetype')),
            ],
        ),
        migrations.RunPython(add_default_package_type),
    ]
