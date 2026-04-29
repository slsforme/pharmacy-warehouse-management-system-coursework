from enum import Enum

from django.core.validators import (
    RegexValidator,
    MinLengthValidator,
    MaxLengthValidator
)

from .regex import *  # noqa

class ValidatorType(Enum):
    STRING_WITH_NUMBERS = "string_with_numbers"
    CYRILLIC_LATIN_ONLY = "cyrillic_latin_only"
    LATIN_ONLY = "latin_only"
    NUMERIC = "numeric"
    MIN_LENGTH = "min_length"
    MAX_LENGTH = "max_length"
    PHONE_NUMBER = "phone_number"
    INN = "inn"
    OKTMO = "oktmo"
    OGRN = "ogrn"
    KPP = "kpp"
    LICENSE = "license"

_VALIDATOR_CONFIG = {
    ValidatorType.STRING_WITH_NUMBERS: {
        "class": RegexValidator,
        "params": {"regex": ONLY_CYRILLIC_LATIN_SPECIAL_SYMBOLS_AND_NUMBERS_STRING_REGEX},
        "message": "{description} должен состоять только из букв, цифр, пробелов и спецсимволов.",
    },
    ValidatorType.CYRILLIC_LATIN_ONLY: {
        "class": RegexValidator,
        "params": {"regex": ONLY_SYMBOLS_STRING_REGEX},
        "message": "{description} должен состоять только из букв и пробелов.",
    },
    ValidatorType.LATIN_ONLY: {
        "class": RegexValidator,
        "params": {"regex": ONLY_LATIN_STRING_REGEX},
        "message": "{description} должен состоять только из латиницы и пробелов.",
    },
    ValidatorType.PHONE_NUMBER: {
        "class": RegexValidator,
        "params": {"regex": PHONE_NUMBER_REGEX},
        "message": "{description} может состоять из цифр, скобок и пробелов.",
    },
    ValidatorType.NUMERIC: {
        "class": RegexValidator,
        "params": {"regex": ONLY_NUMBERS_REGEX},
        "message": "{description} должен состоять только из цифр.",
    },
    ValidatorType.INN: {
        "class": RegexValidator,
        "params": {"regex": INN_REGEX},
        "message": "{description} должен содержать 10 или 12 цифр.",
    },
    ValidatorType.OKTMO: {
        "class": RegexValidator,
        "params": {"regex": OKTMO_REGEX},
        "message": "{description} должен содержать 8 или 11 цифр.",
    },
    ValidatorType.KPP: {
        "class": RegexValidator,
        "params": {"regex": KPP_REGEX},
        "message": "{description} должен содержать 9 цифр.",
    },
    ValidatorType.OGRN: {
        "class": RegexValidator,
        "params": {"regex": OGRN_REGEX},
        "message": "{description} должен содержать 13 или 15 цифр.",
    },
    ValidatorType.LICENSE: {
        "class": RegexValidator,
        "params": {"regex": LICENSE_REGEX},
        "message": "{description} должен иметь формат 'ЛО-77-02-123456'",
    },
    ValidatorType.MIN_LENGTH: {
        "class": MinLengthValidator,
        "params": {}, 
        "message": "{description} должен иметь минимальную длину {limit_value} симв.",
    },
    ValidatorType.MAX_LENGTH: {
        "class": MaxLengthValidator,
        "params": {},
        "message": "{description} должен иметь максимальную длину {limit_value} симв.",
    },
}

def create_validator(validator_type: ValidatorType, description: str , **kwargs):
    config = _VALIDATOR_CONFIG[validator_type]
    validator_class = config["class"]
    params = {**config["params"], **kwargs}
    message = config["message"].format(description=description, **kwargs)
    return validator_class(message=message, **params)


__all__ = ["ValidatorType", "create_validator"]
