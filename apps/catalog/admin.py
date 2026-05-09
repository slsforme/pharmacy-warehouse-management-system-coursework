from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from .models import Drug, DrugGroup, Manufacturer, Supplier


class DrugGroupResource(resources.ModelResource):
    class Meta:
        model = DrugGroup
        fields = ("id", "name", "description")


class ManufacturerResource(resources.ModelResource):
    class Meta:
        model = Manufacturer
        fields = ("id", "name", "country", "phone_number", "email")


class SupplierResource(resources.ModelResource):
    class Meta:
        model = Supplier
        fields = (
            "id", "name", "inn", "ogrn", "kpp", "oktmo",
            "phone_number", "email", "pharma_license_number",
            "pharma_license_date", "pharma_license_expiry",
        )


class DrugResource(resources.ModelResource):
    class Meta:
        model = Drug
        fields = ("id", "name", "group__name", "manufacturer__name")


class CatalogBaseAdmin(ModelAdmin, ImportExportModelAdmin, SimpleHistoryAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm


@admin.register(DrugGroup)
class DrugGroupAdmin(CatalogBaseAdmin):
    resource_class = DrugGroupResource
    list_display = ["name", "created_at", "updated_at"]
    search_fields = ["name"]
    ordering = ["name"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        ("Основное", {"fields": ("name", "description")}),
        ("Служебное", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )


@admin.register(Manufacturer)
class ManufacturerAdmin(CatalogBaseAdmin):
    resource_class = ManufacturerResource
    list_display = ["name", "country", "phone_number", "email", "created_at"]
    search_fields = ["name", "country", "email"]
    list_filter = ["country"]
    ordering = ["name"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        ("Основное", {"fields": ("name", "country")}),
        ("Контакты", {"fields": ("phone_number", "email")}),
        ("Дополнительно", {"fields": ("other_info",)}),
        ("Служебное", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )


@admin.register(Supplier)
class SupplierAdmin(CatalogBaseAdmin):
    resource_class = SupplierResource
    list_display = [
        "name", "inn", "phone_number", "email",
        "is_license_active", "pharma_license_expiry",
    ]
    search_fields = ["name", "inn", "ogrn", "email"]
    ordering = ["name"]
    readonly_fields = ["created_at", "updated_at", "is_license_active"]
    fieldsets = (
        ("Основное", {"fields": ("name", "name_en", "description")}),
        ("Реквизиты", {"fields": ("inn", "kpp", "ogrn", "oktmo")}),
        ("Лицензия", {
            "fields": (
                "pharma_license_number",
                "pharma_license_date",
                "pharma_license_expiry",
                "is_license_active",
            )
        }),
        ("Контакты", {"fields": ("phone_number", "email", "legal_address")}),
        ("Служебное", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )


@admin.register(Drug)
class DrugAdmin(CatalogBaseAdmin):
    resource_class = DrugResource
    list_display = ["name", "group", "manufacturer", "created_at"]
    search_fields = ["name"]
    list_filter = ["group", "manufacturer"]
    list_select_related = ["group", "manufacturer"]
    ordering = ["name"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        ("Основное", {"fields": ("name", "group", "manufacturer")}),
        ("Служебное", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )