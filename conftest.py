import pytest
from django.test import TestCase

@pytest.fixture(autouse=True)
def reset_sequences(db):
    from apps.users.factories import RoleFactory, UserFactory
    from apps.catalog.factories import DrugGroupFactory, DrugFactory, ManufacturerFactory, SupplierFactory
    from apps.inventory.factories import ArrivalFactory, ArrivalItemFactory, StockFactory
    from apps.sales.factories import SaleFactory, SaleItemFactory

    RoleFactory.reset_sequence(0)
    UserFactory.reset_sequence(0)
    DrugGroupFactory.reset_sequence(0)
    DrugFactory.reset_sequence(0)
    ManufacturerFactory.reset_sequence(0)
    SupplierFactory.reset_sequence(0)
    ArrivalFactory.reset_sequence(0)
    ArrivalItemFactory.reset_sequence(0)
    StockFactory.reset_sequence(0)
    SaleFactory.reset_sequence(0)
    SaleItemFactory.reset_sequence(0)
