import logging

from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import permission_classes
from django_filters.rest_framework import DjangoFilterBackend

from .models import Package, PackageType
from .filters import PackageFilter
from .serializers import PackageSerializer, PackageTypeSerializer
from .permissions import IsSessionOwner
from .exceptions import SessionNotCreated


logger = logging.getLogger('apps.api')


class PackagePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PackageCreate(generics.CreateAPIView):
    serializer_class = PackageSerializer


class PackageListFilter(generics.ListAPIView):
    serializer_class = PackageSerializer
    pagination_class = PackagePagination
    filterset_class = PackageFilter

    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        queryset = Package.objects.prefetch_related('package_type')

        session_key = self.request.session.session_key

        if not session_key:
            logger.critical('Session was not created')
            raise SessionNotCreated()

        # TODO: try to filter session owner by drf permissions
        # TODO: order queryset by django-filters
        return queryset.filter(owner_session=session_key).order_by('-pk')


@permission_classes([IsSessionOwner])
class PackageDetail(generics.RetrieveAPIView):
    serializer_class = PackageSerializer
    queryset = Package.objects.prefetch_related('package_type')


class PackageTypeList(generics.ListAPIView):
    queryset = PackageType.objects.all()
    serializer_class = PackageTypeSerializer
