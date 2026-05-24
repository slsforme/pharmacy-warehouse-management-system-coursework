import django
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.catalog.factories import DrugFactory, DrugGroupFactory, ManufacturerFactory, SupplierFactory
from apps.catalog.models import Drug, DrugGroup, Manufacturer, Supplier
from apps.inventory.factories import ArrivalFactory, ArrivalItemFactory, StockFactory
from apps.inventory.models import Arrival, Stock
from apps.sales.factories import SaleFactory, SaleItemFactory
from apps.sales.models import Sale
from apps.users.factories import RoleFactory, UserFactory
from apps.users.models import Role, User


# ===== Fixtures =====
@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def admin_user(db):  
    role, _ = Role.objects.get_or_create(
        name=Role.RoleType.ADMIN,
        defaults={
            "can_manage_catalog": True,
            "can_manage_arrivals": True,
            "can_manage_sales": True,
            "can_view_reports": True,
        }
    )
    return UserFactory(role=role, is_staff=True, is_superuser=True)


@pytest.fixture
def pharmacist(db):  
    role, _ = Role.objects.get_or_create(
        name=Role.RoleType.PHARMACIST,
        defaults={"can_manage_sales": True}
    )
    return UserFactory(role=role)


@pytest.fixture
def storekeeper(db): 
    role, _ = Role.objects.get_or_create(
        name=Role.RoleType.STOREKEEPER,
        defaults={"can_manage_arrivals": True}
    )
    return UserFactory(role=role)



@pytest.fixture
def auth_client(client, admin_user):
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture
def pharmacist_client(client, pharmacist):
    client.force_authenticate(user=pharmacist)
    return client


@pytest.fixture
def storekeeper_client(client, storekeeper):
    client.force_authenticate(user=storekeeper)
    return client


# ===== USERS =====

@pytest.mark.django_db
class TestRoleAPI:
    def test_create_role(self, auth_client):
        data = {
            "name": Role.RoleType.ACCOUNTANT,
            "description": "Бухгалтер",
            "can_view_reports": True,
        }
        response = auth_client.post(reverse("roles-list"), data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Role.objects.filter(name=Role.RoleType.ACCOUNTANT).exists()

    def test_retrieve_role(self, auth_client):
        role = RoleFactory(name=Role.RoleType.STOREKEEPER)
        response = auth_client.get(reverse("roles-detail", args=[role.pk]))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == Role.RoleType.STOREKEEPER

    def test_update_role(self, auth_client):
        role = RoleFactory(name=Role.RoleType.PHARMACIST)
        response = auth_client.patch(
            reverse("roles-detail", args=[role.pk]),
            {"can_manage_sales": True},
        )
        assert response.status_code == status.HTTP_200_OK
        role.refresh_from_db()
        assert role.can_manage_sales is True

    def test_delete_role(self, auth_client):
        role = RoleFactory(name=Role.RoleType.ACCOUNTANT)
        response = auth_client.delete(reverse("roles-detail", args=[role.pk]))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Role.objects.filter(pk=role.pk).exists()

    def test_unauthenticated_access(self, client):
        response = client.get(reverse("roles-list"))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUserAPI:
    def test_list_users(self, auth_client):
        UserFactory.create_batch(3)
        response = auth_client.get(reverse("users-list"))
        assert response.status_code == status.HTTP_200_OK

    def test_create_user(self, auth_client):
        role = RoleFactory(name=Role.RoleType.PHARMACIST)
        data = {
            "email": "newuser@pharmacy.ru",
            "first_name": "Иван",
            "last_name": "Иванов",
            "role": role.pk,
            "password": "testpass123",
        }
        response = auth_client.post(reverse("users-list"), data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email="newuser@pharmacy.ru").exists()

    def test_retrieve_user(self, auth_client, admin_user):
        response = auth_client.get(reverse("users-detail", args=[admin_user.pk]))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == admin_user.email

    def test_update_user(self, auth_client, admin_user):
        response = auth_client.patch(
            reverse("users-detail", args=[admin_user.pk]),
            {"first_name": "Новое имя"},
        )
        assert response.status_code == status.HTTP_200_OK
        admin_user.refresh_from_db()
        assert admin_user.first_name == "Новое имя"

    def test_me_endpoint(self, auth_client, admin_user):
        response = auth_client.get(reverse("users-me"))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == admin_user.email

    def test_password_not_in_response(self, auth_client, admin_user):
        response = auth_client.get(reverse("users-detail", args=[admin_user.pk]))
        assert "password" not in response.data


# ===== CATALOG =====

@pytest.mark.django_db
class TestDrugGroupAPI:
    def test_list(self, auth_client):
        DrugGroupFactory.create_batch(5)
        response = auth_client.get(reverse("drug-groups-list"))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] >= 5

    def test_create(self, auth_client):
        data = {"name": "Антибиотики", "description": "Группа антибиотиков"}
        response = auth_client.post(reverse("drug-groups-list"), data)
        assert response.status_code == status.HTTP_201_CREATED
        assert DrugGroup.objects.filter(name="Антибиотики").exists()

    def test_retrieve(self, auth_client):
        group = DrugGroupFactory(name="Витамины")
        response = auth_client.get(reverse("drug-groups-detail", args=[group.pk]))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Витамины"

    def test_update(self, auth_client):
        group = DrugGroupFactory(name="Старое название")
        response = auth_client.patch(
            reverse("drug-groups-detail", args=[group.pk]),
            {"name": "Новое название"},
        )
        assert response.status_code == status.HTTP_200_OK
        group.refresh_from_db()
        assert group.name == "Новое название"

    def test_delete(self, auth_client):
        group = DrugGroupFactory()
        response = auth_client.delete(reverse("drug-groups-detail", args=[group.pk]))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not DrugGroup.objects.filter(pk=group.pk).exists()

    def test_search(self, auth_client):
        DrugGroupFactory(name="Антибиотики")
        DrugGroupFactory(name="Витамины")
        response = auth_client.get(reverse("drug-groups-list"), {"search": "Анти"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

    def test_unauthenticated(self, client):
        response = client.get(reverse("drug-groups-list"))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestManufacturerAPI:
    def test_list(self, auth_client):
        ManufacturerFactory.create_batch(3)
        response = auth_client.get(reverse("manufacturers-list"))
        assert response.status_code == status.HTTP_200_OK

    def test_create(self, auth_client):
        data = {
            "name": "Фарма Плюс",
            "country": "Россия",
            "phone_number": "+79001234567",
            "email": "pharma@example.com",
        }
        response = auth_client.post(reverse("manufacturers-list"), data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Manufacturer.objects.filter(name="Фарма Плюс").exists()

    def test_retrieve(self, auth_client):
        manufacturer = ManufacturerFactory()
        response = auth_client.get(reverse("manufacturers-detail", args=[manufacturer.pk]))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == manufacturer.name

    def test_update(self, auth_client):
        manufacturer = ManufacturerFactory()
        response = auth_client.patch(
            reverse("manufacturers-detail", args=[manufacturer.pk]),
            {"country": "Германия"},
        )
        assert response.status_code == status.HTTP_200_OK
        manufacturer.refresh_from_db()
        assert manufacturer.country == "Германия"

    def test_delete(self, auth_client):
        manufacturer = ManufacturerFactory()
        response = auth_client.delete(reverse("manufacturers-detail", args=[manufacturer.pk]))
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestSupplierAPI:
    def test_list(self, auth_client):
        SupplierFactory.create_batch(3)
        response = auth_client.get(reverse("suppliers-list"))
        assert response.status_code == status.HTTP_200_OK

    def test_create(self, auth_client):
        data = {
            "name": "Тестовый поставщик ООО",
            "name_en": "Test Supplier LTD",
            "inn": "1234567890",
            "ogrn": "1234567890123",
            "oktmo": "12345678",
            "pharma_license_number": "ЛО-12-82-4254034774",
            "pharma_license_date": "2020-01-01",
            "pharma_license_expiry": "2027-01-01",
            "phone_number": "+79001234500",
            "email": "supplier_new@example.com",
            "legal_address": "г. Москва, ул. Тестовая, д. 1",
        }
        response = auth_client.post(reverse("suppliers-list"), data)

        if response.status_code == 400:
            print(response.data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_license_active_field(self, auth_client):
        supplier = SupplierFactory()
        response = auth_client.get(reverse("suppliers-detail", args=[supplier.pk]))
        assert response.status_code == status.HTTP_200_OK
        assert "is_license_active" in response.data


@pytest.mark.django_db
class TestDrugAPI:
    def test_list(self, auth_client):
        DrugFactory.create_batch(5)
        response = auth_client.get(reverse("drugs-list"))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] >= 5

    def test_create(self, auth_client):
        group = DrugGroupFactory()
        manufacturer = ManufacturerFactory()
        data = {
            "name": "Парацетамол",
            "group": group.pk,
            "manufacturer": manufacturer.pk,
        }
        response = auth_client.post(reverse("drugs-list"), data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Drug.objects.filter(name="Парацетамол").exists()

    def test_filter_by_group(self, auth_client):
        group1 = DrugGroupFactory()
        group2 = DrugGroupFactory()
        DrugFactory.create_batch(3, group=group1)
        DrugFactory.create_batch(2, group=group2)
        response = auth_client.get(reverse("drugs-list"), {"group": group1.pk})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 3

    def test_search(self, auth_client):
        DrugFactory(name="Парацетамол")
        DrugFactory(name="Ибупрофен")
        response = auth_client.get(reverse("drugs-list"), {"search": "Пара"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

    def test_group_name_in_response(self, auth_client):
        drug = DrugFactory()
        response = auth_client.get(reverse("drugs-detail", args=[drug.pk]))
        assert response.status_code == status.HTTP_200_OK
        assert "group_name" in response.data
        assert "manufacturer_name" in response.data


# ===== INVENTORY =====

@pytest.mark.django_db
class TestArrivalAPI:
    def test_list(self, auth_client):
        ArrivalFactory.create_batch(3)
        response = auth_client.get(reverse("arrivals-list"))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] >= 3

    def test_create_with_items(self, storekeeper_client):
        supplier = SupplierFactory()
        drug = DrugFactory()
        data = {
            "supplier": supplier.pk,
            "document_number": "НАК-00001",
            "document_date": "2026-01-01",
            "note": "Тестовая накладная",
            "items": [
                {
                    "drug": drug.pk,
                    "quantity": 100,
                    "price": "50.00",
                    "expiry_date": "2027-01-01",
                    "series": "СЕР-001",
                }
            ],
        }
        response = storekeeper_client.post(reverse("arrivals-list"), data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Arrival.objects.filter(document_number="НАК-00001").exists()
        stock = Stock.objects.get(drug=drug)
        assert stock.quantity == 100

    def test_retrieve(self, auth_client):
        arrival = ArrivalFactory()
        response = auth_client.get(reverse("arrivals-detail", args=[arrival.pk]))
        assert response.status_code == status.HTTP_200_OK
        assert "items" in response.data

    def test_filter_by_supplier(self, auth_client):
        supplier1 = SupplierFactory()
        supplier2 = SupplierFactory()
        ArrivalFactory.create_batch(2, supplier=supplier1)
        ArrivalFactory.create_batch(3, supplier=supplier2)
        response = auth_client.get(reverse("arrivals-list"), {"supplier": supplier1.pk})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2

    def test_unauthenticated(self, client):
        response = client.get(reverse("arrivals-list"))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestStockAPI:
    def test_list(self, auth_client):
        StockFactory.create_batch(5)
        response = auth_client.get(reverse("stock-list"))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] >= 5

    def test_retrieve(self, auth_client):
        stock = StockFactory()
        response = auth_client.get(reverse("stock-detail", args=[stock.pk]))
        assert response.status_code == status.HTTP_200_OK
        assert "drug_name" in response.data
        assert "group_name" in response.data

    def test_stock_is_readonly(self, auth_client):
        drug = DrugFactory()
        data = {"drug": drug.pk, "quantity": 999}
        response = auth_client.post(reverse("stock-list"), data)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_search_by_drug_name(self, auth_client):
        drug1 = DrugFactory(name="Парацетамол")
        drug2 = DrugFactory(name="Ибупрофен")
        StockFactory(drug=drug1)
        StockFactory(drug=drug2)
        response = auth_client.get(reverse("stock-list"), {"search": "Пара"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1


# ===== SALES =====

@pytest.mark.django_db
class TestSaleAPI:
    def test_list(self, auth_client):
        SaleFactory.create_batch(3)
        response = auth_client.get(reverse("sales-list"))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] >= 3

    def test_create_sale(self, pharmacist_client):
        drug = DrugFactory()
        StockFactory(drug=drug, quantity=100)
        data = {
            "note": "Тестовая продажа",
            "items": [
                {
                    "drug": drug.pk,
                    "quantity": "10.00",
                    "price": "150.00",
                }
            ],
        }
        response = pharmacist_client.post(reverse("sales-list"), data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        stock = Stock.objects.get(drug=drug)
        assert stock.quantity == 90

    def test_create_sale_insufficient_stock(self, pharmacist_client):
        drug = DrugFactory()
        StockFactory(drug=drug, quantity=5)
        data = {
            "items": [
                {
                    "drug": drug.pk,
                    "quantity": "100.00",
                    "price": "150.00",
                }
            ],
        }
        response = pharmacist_client.post(reverse("sales-list"), data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_retrieve(self, auth_client, admin_user):
        sale = SaleFactory(cashier=admin_user)
        response = auth_client.get(reverse("sales-detail", args=[sale.pk]))
        assert response.status_code == status.HTTP_200_OK
        assert "items" in response.data
        assert "total" in response.data

    def test_unauthenticated(self, client):
        response = client.get(reverse("sales-list"))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestSaleItemAPI:
    def test_list(self, auth_client, admin_user):
        sale = SaleFactory(cashier=admin_user)
        SaleItemFactory.create_batch(3, sale=sale)
        response = auth_client.get(reverse("sale-items-list"))
        assert response.status_code == status.HTTP_200_OK

    def test_filter_by_sale(self, auth_client, admin_user):
        sale1 = SaleFactory(cashier=admin_user)
        sale2 = SaleFactory(cashier=admin_user)
        SaleItemFactory.create_batch(2, sale=sale1)
        SaleItemFactory.create_batch(3, sale=sale2)
        response = auth_client.get(reverse("sale-items-list"), {"sale": sale1.pk})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2

    def test_total_in_response(self, auth_client, admin_user):
        sale = SaleFactory(cashier=admin_user)
        item = SaleItemFactory(sale=sale, quantity=5, price=200)
        response = auth_client.get(reverse("sale-items-detail", args=[item.pk]))
        assert response.status_code == status.HTTP_200_OK
        assert float(response.data["total"]) == 1000.0