from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from simple_history.models import HistoricalRecords

from common.models import BaseModel
from .managers import UserManager
from common.validators import *


class Role(BaseModel):
    name_min_length = 3
    name_max_length = 50
    class RoleType(models.TextChoices):
        ADMIN = "admin", "Администратор"  # все
        PHARMACIST = "pharmacist", "Фармацевт"  # продажи
        STOREKEEPER = "storekeeper", "Кладовщик"  # приход товара
        ACCOUNTANT = "accountant", "Бухгалтер"  # только отчёты

    name = models.CharField(
        verbose_name="Роль",
        choices=RoleType.choices,
        unique=True,
        blank=False,
        null=False,
        error_messages={
            "unique": f"Такая роль уже существует в системе.",
            "required": "Это поле обязательно",
        },
        validators=[
            create_validator(ValidatorType.STRING_WITH_NUMBERS, "Роль"),
            create_validator(
                ValidatorType.MIN_LENGTH, "Роль", limit_value=name_min_length
            ),
            create_validator(
                ValidatorType.MAX_LENGTH, "Роль", limit_value=name_max_length
            ),
        ],
    )

    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        default="",
    )

    can_manage_catalog = models.BooleanField(default=False, verbose_name="Справочники")
    can_manage_arrivals = models.BooleanField(default=False, verbose_name="Приход")
    can_manage_sales = models.BooleanField(default=False, verbose_name="Продажи")
    can_view_reports = models.BooleanField(default=False, verbose_name="Отчёты")
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    str_min_length: int = 1
    str_max_length: int = 100

    role = models.ForeignKey(
        to="Role",
        on_delete=models.PROTECT,
        verbose_name="Роль",
        null=False,
        blank=False,
    )

    email = models.EmailField(
        verbose_name="Email",
        unique=True,
        null=False,
        blank=False,
    )

    first_name = models.CharField(
        verbose_name="Имя",
        blank=False,
        null=False,
        validators=[
            create_validator(ValidatorType.CYRILLIC_LATIN_ONLY, "Имя"),
            create_validator(
                ValidatorType.MIN_LENGTH, "Имя", limit_value=str_min_length
            ),
            create_validator(
                ValidatorType.MAX_LENGTH, "Имя", limit_value=str_max_length
            ),
        ],
    )

    last_name = models.CharField(
        verbose_name="Фамилия",
        blank=False,
        null=False,
        validators=[
            create_validator(ValidatorType.CYRILLIC_LATIN_ONLY, "Фамилия"),
            create_validator(
                ValidatorType.MIN_LENGTH, "Фамилия", limit_value=str_min_length
            ),
            create_validator(
                ValidatorType.MAX_LENGTH, "Фамилия", limit_value=str_max_length
            ),
        ]
    )

    patronymic = models.CharField(
        verbose_name="Отчество", 
        blank=True, 
        null=True, 
        default="",
        validators=[
            create_validator(ValidatorType.CYRILLIC_LATIN_ONLY, "Отчество"),
            create_validator(
                ValidatorType.MIN_LENGTH, "Отчество", limit_value=str_min_length
            ),
            create_validator(
                ValidatorType.MAX_LENGTH, "Отчество", limit_value=str_max_length
            ),
        ],
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.role.get_name_display()} - {self.full_name}"

    @property
    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name} {self.patronymic}".strip()
