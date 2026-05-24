from rest_framework import serializers
from .models import Arrival, ArrivalItem, Stock


class ArrivalItemSerializer(serializers.ModelSerializer):
    total = serializers.FloatField(read_only=True)
    drug_name = serializers.CharField(source="drug.name", read_only=True)

    class Meta:
        model = ArrivalItem
        fields = [
            "uid", "drug", "drug_name", "quantity",
            "price", "total", "expiry_date", "series",
            "created_at", "updated_at",
        ]
        read_only_fields = ["uid", "total", "created_at", "updated_at"]


class ArrivalSerializer(serializers.ModelSerializer):
    items = ArrivalItemSerializer(many=True, read_only=True)
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)
    created_by_name = serializers.CharField(source="created_by.full_name", read_only=True)

    class Meta:
        model = Arrival
        fields = [
            "uid", "supplier", "supplier_name",
            "created_by", "created_by_name",
            "document_number", "document_date",
            "note", "items", "created_at", "updated_at",
        ]
        read_only_fields = ["uid", "created_at", "updated_at"]


class ArrivalCreateSerializer(serializers.ModelSerializer):
    items = ArrivalItemSerializer(many=True)

    class Meta:
        model = Arrival
        fields = [
            "supplier", "document_number",
            "document_date", "note", "items",
        ]

    def create(self, validated_data):
        from django.db import transaction
        from apps.inventory.models import Stock

        items_data = validated_data.pop("items")

        with transaction.atomic():
            arrival = Arrival.objects.create(
                created_by=self.context["request"].user,
                **validated_data,
            )
            for item_data in items_data:
                ArrivalItem.objects.create(arrival=arrival, **item_data)

                stock, created = Stock.objects.get_or_create(
                    drug=item_data["drug"],
                    defaults={"quantity": 0},
                )
                stock.quantity += item_data["quantity"]
                stock.save()

        return arrival


class StockSerializer(serializers.ModelSerializer):
    drug_name = serializers.CharField(source="drug.name", read_only=True)
    group_name = serializers.CharField(source="drug.group.name", read_only=True)

    class Meta:
        model = Stock
        fields = [
            "uid", "drug", "drug_name", "group_name",
            "quantity", "updated_at",
        ]
        read_only_fields = ["uid", "updated_at"]
