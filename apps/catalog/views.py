from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Drug, DrugGroup, Manufacturer, Supplier
from .serializers import DrugGroupSerializer, DrugSerializer, ManufacturerSerializer, SupplierSerializer


class DrugGroupViewSet(ModelViewSet):
    queryset = DrugGroup.objects.all()
    serializer_class = DrugGroupSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]


class ManufacturerViewSet(ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "country"]
    ordering_fields = ["name", "country"]
    ordering = ["name"]


class SupplierViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name", "inn"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]


class DrugViewSet(ModelViewSet):
    queryset = Drug.objects.select_related("group", "manufacturer").all()
    serializer_class = DrugSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["group", "manufacturer"]
    search_fields = ["name"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]
