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
    NUMERIC = "numeric"
    MIN_LENGTH = "min_length"
    MAX_LENGTH = "max_length"
    PHONE_NUMBER = "phone_number"

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
    ValidatorType.PHONE_NUMBER: {
        "class": RegexValidator,
        "params": {"regex": PHONE_NUMBER_REGEX},
        "message": "{description} может состоять из цифр, скобок и пробелов",
    },
    ValidatorType.NUMERIC: {
        "class": RegexValidator,
        "params": {"regex": ONLY_NUMBERS_REGEX},
        "message": "{description} должен состоять только из цифр.",
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
