from rest_framework import serializers
from .models import Package, PackageType


class PackageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageType
        fields = ('pk', 'name')


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ('pk', 'name', 'weight', 'price', 'package_type')
