from django.contrib import admin
from .models import Sale, SaleItem


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    fields = ["drug", "quantity", "price"]


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ["id", "cashier", "sold_at", "total"]
    list_filter = ["sold_at", "cashier"]
    list_select_related = ["cashier"]
    inlines = [SaleItemInline]