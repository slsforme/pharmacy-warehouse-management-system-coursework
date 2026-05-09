from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.import_export.forms import ExportForm, ImportForm


from .models import Sale, SaleItem


class SaleItemInline(TabularInline):
    model = SaleItem
    extra = 0
    min_num = 1
    fields = ["drug", "quantity", "price", "get_total"]
    readonly_fields = ["get_total"]

    def get_total(self, obj):
        return f"{obj.total:.2f} ₽"
    get_total.short_description = "Сумма"


class SaleResource(resources.ModelResource):
    class Meta:
        model = Sale
        fields = ("id", "cashier__email", "sold_at", "note")


class SaleItemResource(resources.ModelResource):
    class Meta:
        model = SaleItem
        fields = ("id", "sale__id", "drug__name", "quantity", "price")


class SalesBaseAdmin(ModelAdmin, ImportExportModelAdmin, SimpleHistoryAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm


@admin.register(Sale)
class SaleAdmin(SalesBaseAdmin):
    resource_class = SaleResource
    list_display = ["id", "cashier", "sold_at", "get_total", "created_at"]
    search_fields = ["cashier__email", "cashier__first_name"]
    list_filter = ["sold_at", "cashier"]
    list_select_related = ["cashier"]
    ordering = ["-sold_at"]
    readonly_fields = ["sold_at", "created_at", "updated_at", "get_total"]
    inlines = [SaleItemInline]
    fieldsets = (
        ("Продажа", {"fields": ("cashier", "sold_at", "get_total")}),
        ("Примечание", {"fields": ("note",)}),
        ("Служебное", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def get_total(self, obj):
        return f"{obj.total:.2f} ₽"
    get_total.short_description = "Итого"


@admin.register(SaleItem)
class SaleItemAdmin(SalesBaseAdmin):
    resource_class = SaleItemResource
    list_display = ["sale", "drug", "quantity", "price", "get_total"]
    search_fields = ["drug__name"]
    list_filter = ["sale__sold_at"]
    list_select_related = ["sale", "drug"]
    ordering = ["-sale__sold_at"]
    readonly_fields = ["created_at", "updated_at", "get_total"]
    fieldsets = (
        ("Позиция", {"fields": ("sale", "drug", "quantity", "price", "get_total")}),
        ("Служебное", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def get_total(self, obj):
        return f"{obj.total:.2f} ₽"
    get_total.short_description = "Сумма"