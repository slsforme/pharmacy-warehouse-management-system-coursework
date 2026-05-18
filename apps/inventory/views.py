from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Arrival, ArrivalItem, Stock
from .serializers import (
    ArrivalSerializer, ArrivalCreateSerializer,
    ArrivalItemSerializer, StockSerializer,
)


class ArrivalViewSet(ModelViewSet):
    queryset = Arrival.objects.select_related("supplier", "created_by").prefetch_related("items").all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["supplier", "document_date"]
    search_fields = ["document_number", "supplier__name"]
    ordering_fields = ["document_date", "created_at"]
    ordering = ["-document_date"]

    def get_serializer_class(self):
        if self.action == "create":
            return ArrivalCreateSerializer
        return ArrivalSerializer


class ArrivalItemViewSet(ModelViewSet):
    queryset = ArrivalItem.objects.select_related("arrival", "drug").all()
    serializer_class = ArrivalItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["arrival", "drug"]
    search_fields = ["drug__name", "series"]
    ordering = ["-expiry_date"]


class StockViewSet(ReadOnlyModelViewSet):
    queryset = Stock.objects.select_related("drug__group", "drug__manufacturer").all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["drug__group"]
    search_fields = ["drug__name"]
    ordering_fields = ["drug__name", "quantity"]
    ordering = ["drug__name"]
