from django.contrib import admin
from .models import DrugGroup, Drug, Manufacturer, Supplier


@admin.register(DrugGroup)
class DrugGroupAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    search_fields = ["name"]


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ["name", "country", "phone_number", "email"]
    search_fields = ["name", "country"]
    list_filter = ["country"]


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ["name", "inn", "phone_number", "email", "is_license_active"]
    search_fields = ["name", "inn"]
    list_filter = ["pharma_license_expiry"]


@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ["name", "group", "manufacturer"]
    search_fields = ["name"]
    list_filter = ["group", "manufacturer"]
    list_select_related = ["group", "manufacturer"] 