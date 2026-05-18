from django.db import models
from simple_history.models import HistoricalRecords

from common.models import BaseModel
from common.validators import *


class DrugGroup(BaseModel):
    name_max_length: int = 3
    name_min_length: int = 200

    name = models.CharField(
        verbose_name="Наименование",
        null=False,
        blank=False,
        unique=False,
        editable=True,
        error_messages={
            "unique": f"Такое название типа препарата (лекарства) уже существует в системе",
            "required": "Это поле обязательно",
        },
        validators=[
            create_validator(ValidatorType.STRING_WITH_NUMBERS, "Название типа препарата (лекарства)"),
            create_validator(
                ValidatorType.MIN_LENGTH,
                "Название типа препарата (лекарства)",
                limit_value=name_max_length,
            ),
            create_validator(
                ValidatorType.MAX_LENGTH,
                "Название типа препарата (лекарства)",
                limit_value=name_min_length,
            ),
        ],
    )

    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        default="",
        editable=True,
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Manufacturer(BaseModel):
    name_max_length: int = 200
    country_max_length: int = 57
    name_and_country_min_length: int = 3

    name = models.CharField(
        verbose_name="Название",
        null=False,
        blank=False,
        unique=False,
        editable=True,
        error_messages={
            "unique": f"Такое название произодителя уже существует в системе.",
            "required": "Это поле обязательно",
        },
        validators=[
            create_validator(ValidatorType.STRING_WITH_NUMBERS, "Название произодителя"),
            create_validator(
                ValidatorType.MIN_LENGTH,
                "Название произодителя",
                limit_value=name_and_country_min_length,
            ),
            create_validator(
                ValidatorType.MAX_LENGTH,
                "Название произодителя",
                limit_value=name_max_length,
            ),
        ],
    )

    country = models.CharField(
        verbose_name="Страна",
        null=False,
        blank=False,
        unique=False,
        editable=True,
        error_messages={
            "unique": f"Такая страна уже связана с другим производителем.",
            "required": "Это поле обязательно",
        },
        validators=[
            create_validator(
                ValidatorType.CYRILLIC_LATIN_ONLY, "Страна"
            ),
            create_validator(
                ValidatorType.MIN_LENGTH,
                "Страна",
                limit_value=name_and_country_min_length,
            ),
            create_validator(
                ValidatorType.MAX_LENGTH,
                "Страна",
                limit_value=country_max_length,
            ),
        ],
    )

    phone_number = models.CharField(
        verbose_name="Номер телефона",
        null=False,
        blank=False,
        unique=True,
        error_messages={
            "unique": f"Такой номер телефона уже связан с другим производителем.",
            "required": "Эта контактная информация обязательна.",
        },
        validators=[
            create_validator(ValidatorType.PHONE_NUMBER, "Номер телефона"),
        ],
    )

    email = models.EmailField(
        verbose_name="Адрес электронной почты",
        null=False,
        blank=False,
        unique=True,
        error_messages={
            "unique": f"Такой адрес электронной почты уже связан с другим производителем.",
            "required": "Эта контактная информация обязательна.",
        },
    )

    other_info = models.TextField(
        verbose_name="Дополнительная информация",
        blank=True,
        default="",
        editable=True,
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.name



class Supplier(BaseModel):
    name_min_length: int = 3
    name_max_length: int = 255

    name = models.CharField(
        verbose_name="Название поставщика",
        null=False,
        blank=False,
        unique=False,
        editable=True,
        default="...",
        error_messages={
            "unique": f"Такое название поставщика уже существует в системе.",
            "required": "Это поле обязательно",
        },
        validators=[
            create_validator(ValidatorType.STRING_WITH_NUMBERS, "Название поставщика"),
            create_validator(
                ValidatorType.MIN_LENGTH, "Название поставщика", limit_value=name_min_length
            ),
            create_validator(
                ValidatorType.MAX_LENGTH, "Название поставщика", limit_value=name_max_length
            ),
        ],
    )

    name_en = models.CharField(
        verbose_name=f"Название поставщика на английском языке (для заграничных поставщиков)",
        null=True,
        blank=True,
        default="",
        unique=False,
        editable=True,
        error_messages={
            "unique": f"Такое название поставщика уже существует в системе.",
            "required": "Это поле обязательно",
        },
        validators=[
            create_validator(ValidatorType.STRING_WITH_NUMBERS, "Название поставщика"),
            create_validator(
                ValidatorType.MIN_LENGTH, "Название поставщика", limit_value=name_min_length
            ),
            create_validator(
                ValidatorType.MAX_LENGTH, "Название поставщика", limit_value=name_max_length
            ),
        ],
    )

    description = models.TextField(
        blank=True,
        default="",
        editable=True,
    )

    inn = models.CharField(
        verbose_name="ИНН",
        unique=True,
        null=True,
        blank=False,
        validators=[create_validator(ValidatorType.INN, "ИНН")],
    )

    kpp = models.CharField(
        verbose_name="КПП",
        unique=True,
        blank=True,
        null=True,
        validators=[create_validator(ValidatorType.KPP, "КПП")],
    )

    ogrn = models.CharField(
        verbose_name="ОГРН",
        unique=True,
        null=True,
        blank=False,
        validators=[create_validator(ValidatorType.OGRN, "ОГРН")],
    )

    oktmo = models.CharField(
        verbose_name="ОКТМО",
        unique=True,
        blank=False,
        validators=[create_validator(ValidatorType.OKTMO, "ОКТМО")],
    )

    pharma_license_number = models.CharField(
        verbose_name="Номер лицензии (согласно РосЗдравНадзор)",
        null=True,
        unique=True,
        blank=False,
        validators=[create_validator(ValidatorType.LICENSE, "Номер лицензии (согласно РосЗдравНадзор)")],
    )

    pharma_license_date = models.DateField(
        verbose_name="Дата выдачи лицензии",
        null=True,
        blank=False,
    )

    pharma_license_expiry = models.DateField(
        verbose_name="Дата окончания лицензии",
        null=True,
        blank=False,
    )

    legal_address = models.TextField(verbose_name="Юридический адрес", blank=True)

    phone_number = models.CharField(
        verbose_name="Номер телефона",
        null=True,
        unique=True,
        blank=False,
        error_messages={
            "unique": f"Такой номер телефона уже связан с другим поставщиком.",
            "required": "Данная контактная информация обязательна.",
        },
        validators=[
            create_validator(ValidatorType.PHONE_NUMBER, "Номер телефона"),
        ],
    )

    email = models.EmailField(
        verbose_name="Адрес электронной почты",
        null=True,
        unique=True,
        blank=False,
        error_messages={
            "unique": f"Такой адрес электронной почты уже связан с другим поставщиком.",
            "required": "Данная контактная информация обязательна.",
        },
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    @property
    def is_license_active(self):
        from django.utils import timezone

        if self.pharma_license_expiry is None:
            return True

        return self.pharma_license_expiry >= timezone.now().date()


class Drug(BaseModel):
    name_min_length: int = 3
    name_max_length: int = 255

    name = models.CharField(
        verbose_name="Препарат",
        null=False,
        blank=False,
        unique=False,
        editable=True,
        default="...",
        error_messages={
            "unique": f"Такой препарат уже существует в системе.",
            "required": "Это поле обязательно",
        },
        validators=[
            create_validator(ValidatorType.STRING_WITH_NUMBERS, "Препарат"),
            create_validator(
                ValidatorType.MIN_LENGTH, "Препарат", limit_value=name_min_length
            ),
            create_validator(
                ValidatorType.MAX_LENGTH, "Препарат", limit_value=name_max_length
            ),
        ],
    )

    manufacturer = models.ForeignKey(
        to="Manufacturer",
        on_delete=models.PROTECT,
        verbose_name="Произодитель",
        null=True,
        blank=False,
    )

    group = models.ForeignKey(
        to="DrugGroup",
        on_delete=models.PROTECT,
        verbose_name="Группа препаратов",
        null=True,
        blank=False,
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.name
