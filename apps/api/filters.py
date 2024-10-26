from django_filters import rest_framework as filters

from .models import Package, PackageType


class PackageFilter(filters.FilterSet):
    model = Package

    is_processed = filters.BooleanFilter(
        field_name='delivery_price',
        lookup_expr='isnull',
        label='is_processed',
        exclude=True,
    )

    type_id = filters.ModelChoiceFilter(
        field_name='package_type',
        lookup_expr='exact',
        queryset=PackageType.objects.all()
    )
