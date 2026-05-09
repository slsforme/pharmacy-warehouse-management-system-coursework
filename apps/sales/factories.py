import factory
from factory.django import DjangoModelFactory
from faker import Faker

from apps.catalog.models import Drug

from .models import Sale, SaleItem

fake = Faker("ru_RU")


class SaleFactory(DjangoModelFactory):
    class Meta:
        model = Sale

    cashier = factory.Iterator(
        __import__("apps.users.models", fromlist=["User"]).User.objects.all()
    )
    note = factory.LazyFunction(lambda: fake.text(max_nb_chars=100))


class SaleItemFactory(DjangoModelFactory):
    class Meta:
        model = SaleItem

    sale = factory.Iterator(Sale.objects.all())
    drug = factory.Iterator(Drug.objects.all())
    quantity = factory.Sequence(lambda n: n + 1)  # гарантированно > 0
    price = factory.Sequence(lambda n: (n + 1) * 10)  # 10, 20, 30...
