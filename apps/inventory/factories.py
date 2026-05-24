import factory
from django.utils import timezone
from factory.django import DjangoModelFactory
from faker import Faker
import rstr

import uuid

from apps.catalog.models import Drug, Supplier
from apps.catalog.factories import DrugFactory
from apps.catalog.factories import SupplierFactory
from apps.users.factories import UserFactory
from apps.users.models import User

from .models import Arrival, ArrivalItem, Stock


fake = Faker("ru_RU")


class ArrivalFactory(DjangoModelFactory):
    class Meta:
        model = Arrival

    supplier = factory.SubFactory(SupplierFactory)
    document_number = factory.Sequence(lambda d: uuid.uuid4())
    document_date = factory.LazyFunction(timezone.now().date)
    created_by = factory.SubFactory(UserFactory)


class ArrivalItemFactory(DjangoModelFactory):
    class Meta:
        model = ArrivalItem

    arrival = factory.SubFactory(ArrivalFactory)
    drug = factory.SubFactory(DrugFactory)
    quantity = factory.LazyFunction(lambda: fake.random_int(min=1, max=100))
    price = factory.LazyFunction(
        lambda: fake.pydecimal(min_value=10, max_value=5000, right_digits=2)
    )
    expiry_date = factory.LazyFunction(lambda: fake.future_date(end_date="+2y"))
    series = factory.Sequence(lambda n: f"СЕР-{n:04d}")


class StockFactory(DjangoModelFactory):
    class Meta:
        model = Stock
        django_get_or_create = ["drug"]

    drug = factory.SubFactory(DrugFactory)
    quantity = factory.LazyFunction(lambda: fake.random_int(min=0, max=500))
