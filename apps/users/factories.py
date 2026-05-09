import factory
from factory.django import DjangoModelFactory
from faker import Faker

from .models import Role, User

fake = Faker("ru_RU")


class RoleFactory(DjangoModelFactory):
    class Meta:
        model = Role
        django_get_or_create = ["name"]

    name = Role.RoleType.PHARMACIST
    can_manage_sales = True


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ["email"]

    role = factory.Iterator(Role.objects.all())
    email = factory.Sequence(lambda n: f"user{n}@pharmacy.ru")
    first_name = factory.LazyFunction(fake.first_name)
    last_name = factory.LazyFunction(fake.last_name)
    patronymic = factory.LazyFunction(fake.middle_name)
    is_active = True
    password = factory.PostGenerationMethodCall("set_password", "testpass123")
