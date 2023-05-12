from django.shortcuts import render
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models import Package, PackageType
from .serializers import PackageSerializer, PackageTypeSerializer


class PackagePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PackageCreate(generics.CreateAPIView):
    serializer_class = PackageSerializer


class PackageListFilter(generics.ListAPIView):
    serializer_class = PackageSerializer
    pagination_class = PackagePagination

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['package_type']

    queryset = Package.objects.all()


class PackageDetail(generics.RetrieveAPIView):
    serializer_class = PackageSerializer
    queryset = Package.objects.all()


class PackageTypeList(generics.ListAPIView):
    queryset = PackageType.objects.all()
    serializer_class = PackageTypeSerializer
