from django_filters import rest_framework as filters

from .models import Package, PackageType


class PackageFilter(filters.FilterSet):
    model = Package

    is_processed_package = filters.BooleanFilter(
        field_name='delivery_price',
        lookup_expr='isnull',
        label='is_processed_package',
        exclude=True,
    )

    package_type_id = filters.ModelChoiceFilter(
        field_name='package_type',
        lookup_expr='exact',
        queryset=PackageType.objects.all()
    )
