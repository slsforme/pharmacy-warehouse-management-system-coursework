from django.db import models

from common.models import BaseModel
from common.validators import *  # noqa

class DrugGroup(BaseModel):
    name_max_length: int = 3
    name_min_length: int = 200
    name_description_text: str = "Название типа препарата (лекарства)"

    name = models.CharField(
        verbose_name="Наименование",
        null=False,
        blank=False,
        unique=True, 
        editable=True,
        error_messages={
            "unique": f"Такое {name_description_text.lower()} уже существует в системе",
            "required": "Это поле обязательно",
        },
        validators=[
            create_validator(ValidatorType.STRING_WITH_NUMBERS, name_description_text),
            create_validator(ValidatorType.MIN_LENGTH, name_description_text, limit_value=name_max_length),
            create_validator(ValidatorType.MAX_LENGTH, name_description_text, limit_value=name_min_length)
        ],
    )

    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        default="",
        editable=True,
    )


class Manufacturer(BaseModel):
    name_max_length: int = 200
    country_max_length: int = 57
    name_and_country_min_length: int = 3

    country_description_text: str = "Страна"
    name_description_text: str = "Название произодителя"
    phone_number_description_text: str = "Номер телефона"
    email_description_text: str = "Адрес электронной почты"

    name = models.CharField(
        verbose_name="Название",
        null=False,
        blank=False,
        unique=True, 
        editable=True,
        error_messages={
            "unique": f"Такое {name_description_text.lower()} уже существует в системе.",
            "required": "Это поле обязательно",
        },
        validators=[
            create_validator(ValidatorType.STRING_WITH_NUMBERS, name_description_text),
            create_validator(ValidatorType.MIN_LENGTH, name_description_text, limit_value=name_max_length),
            create_validator(ValidatorType.MAX_LENGTH, name_description_text, limit_value=name_and_country_min_length)
        ],
    )
    
    country = models.CharField(
        verbose_name="Страна",
        null=False,
        blank=False,
        unique=True, 
        editable=True,
        error_messages={
            "unique": f"Такая {country_description_text.lower()} уже связана с другим производителем.",
            "required": "Это поле обязательно",
        },
        validators=[
            create_validator(ValidatorType.CYRILLIC_LATIN_ONLY, country_description_text),
            create_validator(ValidatorType.MIN_LENGTH, country_description_text, limit_value=country_max_length),
            create_validator(ValidatorType.MAX_LENGTH, country_description_text, limit_value=name_and_country_min_length)
        ],
    )

    phone_number = models.CharField(
        verbose_name="Номер телефона",
        null=False,
        blank=False,
        unique=True,
        error_messages={
            "unique": f"Такой {phone_number_description_text.lower()} уже связан с другим производителем.",
            "required": "Эта контактная информация обязательна.",
        },
        validators=[
            create_validator(ValidatorType.PHONE_NUMBER, phone_number_description_text),
        ],
    )

    email = models.EmailField(
        verbose_name="Адрес электронной почты",
        null=False,
        blank=False,
        unique=True,
        error_messages={
            "unique": f"Такой {email_description_text.lower()} уже связан с другим производителем.",
            "required": "Эта контактная информация обязательна.",
        },
    )

    other_info = models.TextField(
        verbose_name="Дополнительная информация",
        blank=True,
        default="",
        editable=True,   
    )


class Supplier(BaseModel):
    name_min_length: int = 3
    name_max_length: int = 255
    
    name_text: str = "Название поставщика"
    phone_number_text: str = "Номер телефона"
    email_text: str = "Адрес электронной почты"

    inn_text = "ИНН"
    kpp_text = "КПП"
    ogrn_text = "ОГРН"
    oktmo_text = "ОКТМО"
    license_name_text = "Номер лицензии (согласно РосЗдравНадзор)"

    name = models.CharField(
        verbose_name=name_text,
        null=False,
        blank=False,
        unique=True, 
        editable=True,
        default="...",
        error_messages={
            "unique": f"Такое {name_text.lower()} уже существует в системе.",
            "required": "Это поле обязательно",
        },
        validators=[
            create_validator(ValidatorType.STRING_WITH_NUMBERS, name_text),
            create_validator(ValidatorType.MIN_LENGTH, name_text, limit_value=name_max_length),
            create_validator(ValidatorType.MAX_LENGTH, name_text, limit_value=name_min_length)
        ],
    )

    name_en = models.CharField(
        verbose_name=f"{name_text} на английском языке (для заграничных поставщиков)",
        null=True,
        blank=True,
        default="",
        unique=True, 
        editable=True,
        error_messages={
            "unique": f"Такое {name_text.lower()} уже существует в системе.",
            "required": "Это поле обязательно",
        },
        validators=[
            create_validator(ValidatorType.LATIN_ONLY, name_text),
            create_validator(ValidatorType.MIN_LENGTH, name_text, limit_value=name_max_length),
            create_validator(ValidatorType.MAX_LENGTH, name_text, limit_value=name_min_length)
        ],
    )

    description = models.TextField(
        blank=True,
        default="",
        editable=True,
    )

    inn = models.CharField(
        verbose_name=inn_text,
        unique=True,
        null=True,
        blank=False,
        validators=[create_validator(ValidatorType.INN, inn_text)]
    )

    kpp = models.CharField(
        verbose_name=kpp_text,
        unique=True,
        blank=True,
        null=True,
        validators=[create_validator(ValidatorType.KPP, kpp_text)]
    )

    ogrn = models.CharField(
        verbose_name=ogrn_text,
        unique=True,
        null=True,
        blank=False,
        validators=[create_validator(ValidatorType.OGRN, ogrn_text)]
    )

    oktmo = models.CharField(
        verbose_name=oktmo_text,
        unique=True,
        blank=False,
        validators=[create_validator(ValidatorType.OKTMO, oktmo_text)]
    )

    pharma_license_number = models.CharField(
        verbose_name=license_name_text,
        null=True,
        unique=True,
        blank=False,
        validators=[create_validator(ValidatorType.LICENSE, license_name_text)]
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

    legal_address = models.TextField(
        verbose_name="Юридический адрес",
        blank=True
    )

    phone_number = models.CharField(
        verbose_name=phone_number_text,
        null=True,
        unique=True,
        blank=False,
        error_messages={
            "unique": f"Такой {phone_number_text.lower()} уже связан с другим поставщиком.",
            "required": "Данная контактная информация обязательна.",
        },
        validators=[
            create_validator(ValidatorType.PHONE_NUMBER, phone_number_text),
        ],
    )

    email = models.EmailField(
        verbose_name=email_text,
        null=True,
        unique=True,
        blank=False,
        error_messages={
            "unique": f"Такой {email_text.lower()} уже связан с другим поставщиком.",
            "required": "Данная контактная информация обязательна.",
        },
    )

    @property
    def is_license_active(self):
        from django.utils import timezone
        if self.pharma_license_expiry is None:
            return True
        
        return self.pharma_license_expiry >= timezone.now().date()

class Drug(BaseModel):
    name_min_length: int = 3
    name_max_length: int = 255

    name_text = "Препарат"


    name = models.CharField(
        verbose_name=name_text,
        null=False,
        blank=False,
        unique=True, 
        editable=True,
        default="...",
        error_messages={
            "unique": f"Такой {name_text.lower()} уже существует в системе.",
            "required": "Это поле обязательно",
        },
        validators=[
            create_validator(ValidatorType.STRING_WITH_NUMBERS, name_text),
            create_validator(ValidatorType.MIN_LENGTH, name_text, limit_value=name_max_length),
            create_validator(ValidatorType.MAX_LENGTH, name_text, limit_value=name_min_length)
        ],
    )

    manufacturer = models.ForeignKey(
        to="Manufacturer",
        on_delete=models.PROTECT,
        verbose_name="Произодитель",
        null=True,
        blank=False
    )

