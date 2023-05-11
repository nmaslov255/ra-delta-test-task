from django.shortcuts import render
from rest_framework import generics

from .models import Package, PackageType
from .serializers import PackageSerializer, PackageTypeSerializer


class PackageTypeList(generics.ListAPIView):
    queryset = PackageType.objects.all()
    serializer_class = PackageTypeSerializer

class PackageListCreate(generics.ListCreateAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
