from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Sale, SaleItem
from .serializers import SaleSerializer, SaleCreateSerializer, SaleItemSerializer


class SaleViewSet(ModelViewSet):
    queryset = Sale.objects.select_related("cashier").prefetch_related("items__drug").all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["cashier", "sold_at"]
    search_fields = ["cashier__email"]
    ordering_fields = ["sold_at", "created_at"]
    ordering = ["-sold_at"]

    def get_serializer_class(self):
        if self.action == "create":
            return SaleCreateSerializer
        return SaleSerializer


class SaleItemViewSet(ModelViewSet):
    queryset = SaleItem.objects.select_related("sale", "drug").all()
    serializer_class = SaleItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["sale", "drug"]
    search_fields = ["drug__name"]
    ordering = ["-sale__sold_at"]
