from django.db import models
from simple_history.models import HistoricalRecords

from common.models import BaseModel
from common.validators import *


class Arrival(BaseModel):
    doc_min_length: int = 3
    doc_max_length: int = 100

    supplier = models.ForeignKey(
        to="catalog.Supplier",
        on_delete=models.PROTECT,
        verbose_name="Поставщик",
        null=False,
        blank=False,
    )

    created_by = models.ForeignKey(
        to="users.User",
        on_delete=models.PROTECT,
        verbose_name="Кто принял",
        null=True,
    )

    document_number = models.CharField(
        verbose_name="Номер документа", 
        unique=False, 
        null=False, 
        blank=False,
        validators=[
            create_validator(ValidatorType.STRING_WITH_NUMBERS, "Номер документа"),
            create_validator(
                ValidatorType.MIN_LENGTH, "Номер документа", limit_value=doc_min_length
            ),
            create_validator(
                ValidatorType.MAX_LENGTH, "Номер документа", limit_value=doc_max_length
            ),
        ],
    )

    document_date = models.DateField(
        verbose_name="Дата документа",
        db_index=True,
        null=False,
        blank=False,
    )

    note = models.TextField(
        verbose_name="Примечание",
        blank=True,
        default="",
    )

    def __str__(self):
        return f"Поставка по документу № {self.document_number}"


class ArrivalItem(BaseModel):
    arrival = models.ForeignKey(
        to="Arrival",
        on_delete=models.CASCADE,
        verbose_name="Приход",
        related_name="items",
    )

    drug = models.ForeignKey(
        to="catalog.Drug",
        on_delete=models.PROTECT,
        verbose_name="Препарат",
    )

    quantity = models.IntegerField(
        verbose_name="Количество",
        null=False,
        blank=False,
    )

    price = models.DecimalField(
        verbose_name="Цена закупки",
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False,
    )

    expiry_date = models.DateField(
        verbose_name="Срок годности",
        db_index=True,
        null=False,
        blank=False,
    )

    series = models.CharField(
        verbose_name="Серия препарата",
        null=False,
        blank=False,
        
    )

    history = HistoricalRecords()

    def __str__(self):
        return f"Поставка препара '{self.drug.name}'"

    @property
    def total(self) -> float:
        return self.quantity * self.price


class Stock(BaseModel):
    drug = models.OneToOneField(
        to="catalog.Drug",
        on_delete=models.PROTECT,
        verbose_name="Препарат",
    )

    quantity = models.IntegerField(
        verbose_name="Остаток",
        null=False,
        blank=False
    )

    history = HistoricalRecords()
    
    def __str__(self):
        return f"Наличие препарата '{self.drug.name}'"
