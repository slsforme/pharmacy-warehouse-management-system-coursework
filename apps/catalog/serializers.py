from rest_framework import serializers
from .models import Drug, DrugGroup, Manufacturer, Supplier


class DrugGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugGroup
        fields = ["uid", "name", "description", "created_at", "updated_at"]
        read_only_fields = ["uid", "created_at", "updated_at"]


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = [
            "uid", "name", "country", "phone_number",
            "email", "other_info", "created_at", "updated_at",
        ]
        read_only_fields = ["uid", "created_at", "updated_at"]


class SupplierSerializer(serializers.ModelSerializer):
    is_license_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Supplier
        fields = [
            "uid", "name", "name_en", "description",
            "inn", "kpp", "ogrn", "oktmo",
            "pharma_license_number", "pharma_license_date", "pharma_license_expiry",
            "is_license_active", "legal_address", "phone_number", "email",
            "created_at", "updated_at",
        ]
        read_only_fields = ["uid", "created_at", "updated_at", "is_license_active"]


class DrugSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source="group.name", read_only=True)
    manufacturer_name = serializers.CharField(source="manufacturer.name", read_only=True)

    class Meta:
        model = Drug
        fields = [
            "uid", "name", "group", "group_name",
            "manufacturer", "manufacturer_name",
            "created_at", "updated_at",
        ]
        read_only_fields = ["uid", "created_at", "updated_at"]