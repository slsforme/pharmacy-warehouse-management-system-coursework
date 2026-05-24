from decimal import Decimal
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

from apps.catalog.models import Drug, DrugGroup
from apps.inventory.models import Stock, Arrival
from apps.sales.models import Sale, SaleItem


def get_dashboard_data() -> dict:
    today = timezone.now().date()
    month_start = today.replace(day=1)

    summary = {
        "total_drugs":      Drug.objects.count(),
        "total_groups":     DrugGroup.objects.count(),
        "total_arrivals":   Arrival.objects.count(),
        "total_sales":      Sale.objects.count(),
        "sales_this_month": Sale.objects.filter(sold_at__date__gte=month_start).count(),
        "low_stock_count":  Stock.objects.filter(quantity__lte=10).count(),
        "out_of_stock":     Stock.objects.filter(quantity=0).count(),
    }

    stock_by_group = list(
        Stock.objects
        .select_related("drug__group")
        .values("drug__group__name")
        .annotate(total=Sum("quantity"))
        .order_by("-total")
    )

    sales_last_30 = []
    for i in range(29, -1, -1):
        day = today - timedelta(days=i)
        count = Sale.objects.filter(sold_at__date=day).count()
        sales_last_30.append({"date": day.strftime("%d.%m"), "count": count})

    top_drugs = list(
        SaleItem.objects
        .filter(sale__sold_at__date__gte=month_start)
        .values("drug__name")
        .annotate(
            total_quantity=Sum("quantity"),
        )
        .order_by("-total_quantity")[:10]
    )

    return {
        "summary":        summary,
        "stock_by_group": stock_by_group,
        "sales_last_30":  sales_last_30,
        "top_drugs":      top_drugs,
    }