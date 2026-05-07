from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from common.models import BaseModel
from .managers import UserManager


class Role(BaseModel):
    class RoleType(models.TextChoices):
        ADMIN       = "admin",      "Администратор"
        PHARMACIST  = "pharmacist", "Фармацевт"       # продажи
        STOREKEEPER = "storekeeper","Кладовщик"        # приход товара
        ACCOUNTANT  = "accountant", "Бухгалтер"        # только отчёты

    name = models.CharField(
        verbose_name="Роль",
        max_length=50,
        choices=RoleType.choices,
        unique=True,
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        default="",
    )

    # Права доступа к разделам
    can_manage_catalog  = models.BooleanField(default=False, verbose_name="Справочники")
    can_manage_arrivals = models.BooleanField(default=False, verbose_name="Приход")
    can_manage_sales    = models.BooleanField(default=False, verbose_name="Продажи")
    can_view_reports    = models.BooleanField(default=False, verbose_name="Отчёты")


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    role = models.ForeignKey(
        to="Role",
        on_delete=models.PROTECT,
        verbose_name="Роль",
        null=True,
        blank=False,
    )

    email = models.EmailField(
        verbose_name="Email",
        unique=True,
        null=False,
        blank=False,
    )
    first_name = models.CharField(verbose_name="Имя", max_length=100)
    last_name  = models.CharField(verbose_name="Фамилия", max_length=100)
    patronymic = models.CharField(verbose_name="Отчество", max_length=100, blank=True, default="")

    is_active = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=False)

    USERNAME_FIELD  = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    @property
    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name} {self.patronymic}".strip()