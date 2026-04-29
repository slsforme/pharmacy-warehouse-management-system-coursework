from django.db import models
from django.core.validators import (
    RegexValidator,
    MinLengthValidator,
    MaxLengthValidator
)

from common.models import BaseModel
from common.validators import *  # noqa

class DrugGroup(BaseModel):
    name_max_length: int = 3
    name_min_length: int = 200
    name_description_text: str = "Название типа препарата (лекарства)"

    name = models.CharField(
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
        null=False,
        blank=False,
        unique=True,
        error_messages={
            "unique": f"Такой {email_description_text.lower()} уже связан с другим производителем.",
            "required": "Эта контактная информация обязательна.",
        },
    )

    other_info = models.TextField(
        blank=True,
        default="",
        editable=True,   
    )


class Supplier(BaseModel):
    name = ...
    name_en = ... 
    description = ...
    inn = ...
    kpp = ...
    ogrn = ...
    oktmo = ...
    pharma_license_number = ...
    pharma_license_date = ...
    pharma_license_expiry = ...
    legal_address = ...
    phone_number = ...
    email = ...

