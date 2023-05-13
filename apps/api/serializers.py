from django.contrib.sessions.models import Session
from rest_framework import serializers

from .models import Package, PackageType
from .exceptions import SessionNotCreated


class PackageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageType
        fields = ('pk', 'name')


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package

        read_only_fields = ('delivery_price',)
        fields = ('pk', 'name', 'weight', 'price', 'delivery_price',
                  'package_type')


    def create(self, validated_data):
        request = self.context.get('request')
        session_key = request.session.session_key
        session = Session.objects.get(session_key=session_key)

        if not session_key:
            raise SessionNotCreated()

        validated_data['owner_session'] = session

        validated_data.pop('delivery_price', None)

        return super().create(validated_data)

    def to_representation(self, instance):
        package = super().to_representation(instance)

        # I hardcoded this because I don't want to overload the model
        # with foreign keys. We can create UnitModel and CurrencyModel
        # in the future...
        package['weight_unit'] = 'gram'
        package['price_currency'] = 'usd'
        package['delivery_currency'] = 'rub'

        return package
