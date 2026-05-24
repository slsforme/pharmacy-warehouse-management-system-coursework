import factory
from factory.django import DjangoModelFactory
from faker import Faker
import rstr

from .models import Drug, DrugGroup, Manufacturer, Supplier

from common.regex import LICENSE_REGEX

fake = Faker("ru_RU")


class DrugGroupFactory(DjangoModelFactory):
    class Meta:
        model = DrugGroup
        django_get_or_create = ["name"]

    name = factory.Sequence(lambda n: f"Группа препаратов {n}")
    description = factory.LazyFunction(lambda: fake.text(max_nb_chars=200))


class ManufacturerFactory(DjangoModelFactory):
    class Meta:
        model = Manufacturer
        django_get_or_create = ["phone_number"]

    name = factory.Sequence(lambda n: f"Производитель {n}")
    country = factory.Sequence(lambda n: fake.country)
    phone_number = factory.Sequence(
        lambda n: f"+7{n:010d}"
    )
    email = factory.Sequence(lambda n: f"manufacturer{n}@example.com")
    other_info = factory.LazyFunction(lambda: fake.text(max_nb_chars=200))


class SupplierFactory(DjangoModelFactory):
    class Meta:
        model = Supplier
        django_get_or_create = ["inn"]

    name = factory.Sequence(lambda n: f"Поставщик {n}")
    name_en = factory.Sequence(lambda n: f"Supplier{n}")
    description = factory.LazyFunction(lambda: fake.text(max_nb_chars=200))

    inn = factory.Sequence(lambda n: f"{n:010d}")
    kpp = factory.Sequence(lambda n: f"{n:09d}")
    ogrn = factory.Sequence(lambda n: f"{n:013d}")
    oktmo = factory.Sequence(lambda n: f"{n:08d}")

    pharma_license_number = factory.Sequence(lambda n: rstr.xeger(LICENSE_REGEX))

    pharma_license_date = factory.LazyFunction(
        lambda: fake.date_between(start_date="-5y", end_date="-1y")
    )
    pharma_license_expiry = factory.LazyFunction(
        lambda: fake.date_between(start_date="+1y", end_date="+3y")
    )

    legal_address = factory.LazyFunction(lambda: fake.address())
    phone_number = factory.Sequence(lambda n: f"+7{n:010d}")
    email = factory.Sequence(lambda n: f"supplier{n}@example.com")


class DrugFactory(DjangoModelFactory):
    class Meta:
        model = Drug
        django_get_or_create = ["name"]

    name = factory.Sequence(lambda n: f"Препарат {n}")
    group = factory.SubFactory(DrugGroupFactory)
    manufacturer = factory.SubFactory(ManufacturerFactory)
