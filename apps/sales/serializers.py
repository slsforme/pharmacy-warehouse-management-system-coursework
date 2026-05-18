from rest_framework import serializers
from .models import Sale, SaleItem


class SaleItemSerializer(serializers.ModelSerializer):
    total = serializers.FloatField(read_only=True)
    drug_name = serializers.CharField(source="drug.name", read_only=True)

    class Meta:
        model = SaleItem
        fields = [
            "uid", "drug", "drug_name",
            "quantity", "price", "total",
            "created_at", "updated_at",
        ]
        read_only_fields = ["uid", "total", "created_at", "updated_at"]


class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True, read_only=True)
    total = serializers.FloatField(read_only=True)
    cashier_name = serializers.CharField(source="cashier.full_name", read_only=True)

    class Meta:
        model = Sale
        fields = [
            "uid", "cashier", "cashier_name",
            "sold_at", "note", "total", "items",
            "created_at", "updated_at",
        ]
        read_only_fields = ["uid", "sold_at", "total", "created_at", "updated_at"]


class SaleCreateSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)

    class Meta:
        model = Sale
        fields = ["note", "items"]

    def create(self, validated_data):
        from django.db import transaction
        from apps.inventory.models import Stock

        items_data = validated_data.pop("items")

        with transaction.atomic():
            sale = Sale.objects.create(
                cashier=self.context["request"].user,
                **validated_data,
            )
            for item_data in items_data:
                # Проверяем остатки
                stock = Stock.objects.select_for_update().get(drug=item_data["drug"])
                if stock.quantity < item_data["quantity"]:
                    raise serializers.ValidationError(
                        f"Недостаточно товара: {stock.drug.name}. "
                        f"Доступно: {stock.quantity}"
                    )
                SaleItem.objects.create(sale=sale, **item_data)
                stock.quantity -= item_data["quantity"]
                stock.save()

        return sale
