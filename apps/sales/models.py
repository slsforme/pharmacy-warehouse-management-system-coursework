from django.db import models
from simple_history.models import HistoricalRecords

from common.models import BaseModel


class Sale(BaseModel):
    cashier = models.ForeignKey(
        to="users.User",
        on_delete=models.PROTECT,
        verbose_name="Кассир",
        null=False,
        blank=False
    )

    sold_at = models.DateTimeField(
        verbose_name="Дата продажи",
        db_index=True,
        auto_now_add=True,
    )

    note = models.TextField(
        verbose_name="Примечание",
        blank=True,
        editable=True,
        default="",
    )

    history = HistoricalRecords()

    def __str__(self):
        return f"Чек № {self.uid}"

    @property
    def total(self) -> float:
        return sum(item.total for item in self.items.all())


class SaleItem(BaseModel):
    sale = models.ForeignKey(
        to="Sale",
        on_delete=models.CASCADE,
        verbose_name="Продажа",
        related_name="items",
    )
    
    drug = models.ForeignKey(
        to="catalog.Drug",
        on_delete=models.PROTECT,
        verbose_name="Препарат",
    )

    quantity = models.DecimalField(
        verbose_name="Количество",
        max_digits=10,
        decimal_places=2,
    )

    price = models.DecimalField(
        verbose_name="Цена продажи",
        max_digits=10,
        decimal_places=2,
    )

    history = HistoricalRecords()

    def __str__(self):
        return f"Продажа {self.drug.name}"

    @property
    def total(self) -> float:
        if self.quantity is None or self.price is None:
            return 0
        return self.quantity * self.price
