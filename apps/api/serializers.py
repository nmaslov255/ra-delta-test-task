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
        fields = ('pk', 'name', 'weight', 'price', 'package_type')

    def create(self, validated_data):
        request = self.context.get('request')
        session_key = request.session.session_key
        session = Session.objects.get(session_key=session_key)

        if not session_key:
            raise SessionNotCreated()

        validated_data['owner_session'] = session
        return super().create(validated_data)
