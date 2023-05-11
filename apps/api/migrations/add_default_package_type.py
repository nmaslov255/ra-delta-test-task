from django.db import migrations


def add_default_package_type(apps, schema_editor):
    PackageType = apps.get_model("api", "PackageType")

    PackageType.objects.get_or_create(name='Other')
    PackageType.objects.get_or_create(name='Electronics')
    PackageType.objects.get_or_create(name='Clothing')


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_default_package_type),
    ]

