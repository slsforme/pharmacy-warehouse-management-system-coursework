from decimal import Decimal

from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from django.db.models.functions import Coalesce

from apps.catalog.models import DrugGroup
from apps.inventory.models import Stock
from apps.sales.models import SaleItem


amount_expr = ExpressionWrapper(
    F("quantity") * F("price"),
    output_field=DecimalField(max_digits=10, decimal_places=2)
)


def get_stock_by_group() -> list[dict]:
    groups = DrugGroup.objects.prefetch_related(
        "drug_set__stock"
    ).all()

    result = []

    for group in groups:
        drugs = []

        for drug in group.drug_set.all():
            try:
                quantity = drug.stock.quantity
            except Stock.DoesNotExist:
                quantity = 0

            drugs.append({
                "name": drug.name,
                "quantity": quantity,
            })

        total = sum(d["quantity"] for d in drugs)

        result.append({
            "group": group.name,
            "drugs": drugs,
            "total": total,
        })

    return result


def get_sales_by_group(date_from, date_to) -> list[dict]:
    items = (
        SaleItem.objects
        .filter(sale__sold_at__date__range=[date_from, date_to])
        .select_related("drug__group", "drug")
    )

    # Группируем в Python
    groups = {}
    for item in items:
        group_name = item.drug.group.name if item.drug.group else "Без группы"

        if group_name not in groups:
            groups[group_name] = {
                "group": group_name,
                "total_quantity": 0,
                "total_amount": Decimal("0"),
                "drugs": {},
            }

        drug_name = item.drug.name
        if drug_name not in groups[group_name]["drugs"]:
            groups[group_name]["drugs"][drug_name] = {
                "drug__name": drug_name,
                "quantity": 0,
                "amount": Decimal("0"),
            }

        quantity = item.quantity or 0
        price = item.price or Decimal("0")
        amount = quantity * price

        groups[group_name]["total_quantity"] += quantity
        groups[group_name]["total_amount"] += amount
        groups[group_name]["drugs"][drug_name]["quantity"] += quantity
        groups[group_name]["drugs"][drug_name]["amount"] += amount

    result = []
    for group_data in groups.values():
        result.append({
            "group":          group_data["group"],
            "total_quantity": group_data["total_quantity"],
            "total_amount":   group_data["total_amount"],
            "drugs":          list(group_data["drugs"].values()),
        })

    return sorted(result, key=lambda x: x["group"])


def get_arrival_for_invoice(arrival_id: int) -> dict:
    from apps.inventory.models import Arrival

    arrival = (
        Arrival.objects
        .select_related("supplier", "created_by")
        .prefetch_related("items__drug")
        .get(pk=arrival_id)
    )

    items = []
    for item in arrival.items.all():
        items.append({
            "name":        item.drug.name,
            "series":      item.series,
            "expiry_date": item.expiry_date,
            "quantity":    item.quantity,
            "price":       item.price,
            "total":       item.total,
        })

    return {
        "document_number":  arrival.document_number,
        "document_date":    arrival.document_date,
        "supplier":         arrival.supplier.name,
        "supplier_inn":     arrival.supplier.inn,
        "supplier_address": arrival.supplier.legal_address,
        "created_by":       arrival.created_by.full_name if arrival.created_by else "",
        "items":            items,
        "grand_total":      sum(i["total"] for i in items),
    }