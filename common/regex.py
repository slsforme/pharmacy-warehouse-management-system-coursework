SPECIAL_CHARS = r"!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?`~\s"

ONLY_CYRILLIC_LATIN_SPECIAL_SYMBOLS_AND_NUMBERS_STRING_REGEX = (
    rf"^[а-яА-ЯёЁa-zA-Z\d{SPECIAL_CHARS}]+$"
)

ONLY_SYMBOLS_AND_SPECIAL_SYMBOLS_STRING_REGEX = rf"^[а-яА-ЯёЁa-zA-Z{SPECIAL_CHARS}]+$"

ONLY_SYMBOLS_STRING_REGEX = r"^[а-яА-ЯёЁa-zA-Z\s]+$"

ONLY_CYRILLIC_STRING_REGEX = r"^[а-яА-ЯёЁ\s]+$"

ONLY_LATIN_STRING_REGEX = r"^[a-zA-Z\s]+$"

ONLY_NUMBERS_REGEX = r"^\d+$"

PHONE_NUMBER_REGEX = r"^(\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$"

INN_REGEX = r"^\d{10}(\d{2})?$"

KPP_REGEX = r"^\d{9}$"

OGRN_REGEX = r"^\d{13}(\d{2})?$"

OKTMO_REGEX = r"^\d{8}(\d{3})?$"

LICENSE_REGEX = r"^ЛО-\d{2}-\d{2}-\d{10}$"

__all__ = [
    "ONLY_CYRILLIC_LATIN_SPECIAL_SYMBOLS_AND_NUMBERS_STRING_REGEX",
    "ONLY_SYMBOLS_AND_SPECIAL_SYMBOLS_STRING_REGEX",
    "ONLY_SYMBOLS_STRING_REGEX",
    "ONLY_CYRILLIC_STRING_REGEX",
    "ONLY_LATIN_STRING_REGEX",
    "PHONE_NUMBER_REGEX",
    "ONLY_NUMBERS_REGEX",
    "OGRN_REGEX",
    "OKTMO_REGEX",
    "INN_REGEX",
    "KPP_REGEX",
    "LICENSE_REGEX",
]
