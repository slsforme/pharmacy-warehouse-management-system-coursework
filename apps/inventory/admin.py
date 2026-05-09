from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from .models import Arrival, ArrivalItem, Stock


class ArrivalItemInline(TabularInline):
    model = ArrivalItem
    extra = 0
    min_num = 1
    fields = ["drug", "quantity", "price", "expiry_date", "series", "get_total"]
    readonly_fields = ["get_total"]

    def get_total(self, obj):
        return f"{obj.total:.2f} ₽"
    get_total.short_description = "Сумма"


class ArrivalResource(resources.ModelResource):
    class Meta:
        model = Arrival
        fields = ("id", "supplier__name", "document_number", "document_date", "created_by__email")


class ArrivalItemResource(resources.ModelResource):
    class Meta:
        model = ArrivalItem
        fields = ("id", "arrival__document_number", "drug__name", "quantity", "price", "expiry_date", "series")


class StockResource(resources.ModelResource):
    class Meta:
        model = Stock
        fields = ("id", "drug__name", "quantity")


class InventoryBaseAdmin(ModelAdmin, ImportExportModelAdmin, SimpleHistoryAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm


@admin.register(Arrival)
class ArrivalAdmin(InventoryBaseAdmin):
    resource_class = ArrivalResource
    list_display = ["document_number", "supplier", "document_date", "created_by", "created_at"]
    search_fields = ["document_number", "supplier__name"]
    list_filter = ["supplier", "document_date"]
    list_select_related = ["supplier", "created_by"]
    ordering = ["-document_date"]
    readonly_fields = ["created_at", "updated_at"]
    inlines = [ArrivalItemInline]
    fieldsets = (
        ("Документ", {"fields": ("document_number", "document_date")}),
        ("Поставщик", {"fields": ("supplier", "created_by")}),
        ("Примечание", {"fields": ("note",)}),
        ("Служебное", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )


@admin.register(ArrivalItem)
class ArrivalItemAdmin(InventoryBaseAdmin):
    resource_class = ArrivalItemResource
    list_display = ["arrival", "drug", "quantity", "price", "expiry_date", "series", "get_total"]
    search_fields = ["drug__name", "series"]
    list_filter = ["expiry_date"]
    list_select_related = ["arrival", "drug"]
    ordering = ["-expiry_date"]
    readonly_fields = ["created_at", "updated_at", "get_total"]
    fieldsets = (
        ("Позиция", {"fields": ("arrival", "drug", "quantity", "price", "expiry_date", "series", "get_total")}),
        ("Служебное", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def get_total(self, obj):
        return f"{obj.total:.2f} ₽"
    get_total.short_description = "Сумма"


@admin.register(Stock)
class StockAdmin(InventoryBaseAdmin):
    resource_class = StockResource
    list_display = ["drug", "quantity", "updated_at"]
    search_fields = ["drug__name"]
    list_select_related = ["drug"]
    ordering = ["drug__name"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        ("Остаток", {"fields": ("drug", "quantity")}),
        ("Служебное", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )