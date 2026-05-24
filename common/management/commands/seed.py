from django.core.management.base import BaseCommand

from apps.catalog.factories import (
    DrugFactory,
    DrugGroupFactory,
    ManufacturerFactory,
    SupplierFactory,
)
from apps.catalog.models import Drug, DrugGroup, Manufacturer, Supplier
from apps.inventory.factories import ArrivalFactory, ArrivalItemFactory, StockFactory
from apps.inventory.models import Arrival, ArrivalItem, Stock
from apps.sales.factories import SaleFactory, SaleItemFactory
from apps.sales.models import Sale, SaleItem
from apps.users.factories import RoleFactory, UserFactory
from apps.users.models import Role, User


class Command(BaseCommand):
    help = "Заполняет БД тестовыми данными"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=20)
        parser.add_argument("--flush", action="store_true", default=True)

    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        
        if kwargs["flush"]:
            self.stdout.write("Cleaning Database...")
            SaleItem.objects.all().delete()
            Sale.objects.all().delete()
            ArrivalItem.objects.all().delete()
            Stock.objects.all().delete()
            Arrival.objects.all().delete()
            Drug.objects.all().delete()
            Supplier.objects.all().delete()
            Manufacturer.objects.all().delete()
            DrugGroup.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write("Models were deleted succesfully")

        for role in Role.RoleType:
            RoleFactory(name=role)
        UserFactory.create_batch(5)

        DrugGroupFactory.create_batch(count)
        ManufacturerFactory.create_batch(count)
        SupplierFactory.create_batch(count)

        DrugFactory.create_batch(count)

        StockFactory.create_batch(count)
        ArrivalFactory.create_batch(count)
        ArrivalItemFactory.create_batch(count)

        SaleFactory.create_batch(count)
        SaleItemFactory.create_batch(count)

        self.stdout.write("Models were created succesfully")
