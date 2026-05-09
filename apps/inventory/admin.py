from django.contrib import admin

from .models import Arrival, ArrivalItem, Stock


class ArrivalItemInline(admin.TabularInline):
    model = ArrivalItem
    extra = 1
    fields = ["drug", "quantity", "price", "expiry_date", "series"]


@admin.register(Arrival)
class ArrivalAdmin(admin.ModelAdmin):
    list_display = ["document_number", "supplier", "document_date", "created_at"]
    search_fields = ["document_number"]
    list_filter = ["supplier", "document_date"]
    inlines = [ArrivalItemInline]  # позиции прямо внутри накладной


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ["drug", "quantity", "updated_at"]
    search_fields = ["drug__name"]
    list_select_related = ["drug"]
