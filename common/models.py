import logging
import re
import uuid

from deep_translator import GoogleTranslator
from django.db import models
from mawo_pymorphy3 import create_analyzer

VERBOSE_NAME_OVERRIDES: dict[str, tuple[str, str]] = {
    "DrugGroup": ("группа препаратов", "группы препаратов"),
    "Sale": ("продажа", "продажи"),
    "Stock": ("остаток на складе", "остатки на складе"),
}

logging.getLogger("mawo_pymorphy3").setLevel(logging.CRITICAL)
logging.getLogger("dawg_dictionary").setLevel(logging.CRITICAL)

analyzer = create_analyzer()
translator = GoogleTranslator(source="en", target="ru")


def _camel_to_words(name: str) -> str:
    words = re.findall(r"[A-Z][a-z]*", name)
    return " ".join(words)


def _translate(text: str) -> str:
    return translator.translate(text).lower()


def _inflect(word: str, grammemes: set) -> str:
    parsed = analyzer.parse(word)[0]
    result = parsed.inflect(grammemes)
    return result.word if result else word


def _generate_verbose_names(class_name: str) -> tuple[str, str]:
    if class_name in VERBOSE_NAME_OVERRIDES:
        return VERBOSE_NAME_OVERRIDES[class_name]

    words_en = _camel_to_words(class_name)
    translated = _translate(words_en)

    singular_parts, plural_parts = [], []
    for word in translated.split():
        singular_parts.append(_inflect(word, {"nomn", "sing"}))
        plural_parts.append(_inflect(word, {"nomn", "plur"}))

    return " ".join(singular_parts), " ".join(plural_parts)


class BaseModelMeta(models.base.ModelBase):
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)

        # Пропускаем абстрактные модели
        if cls._meta.abstract:
            return cls

        singular, plural = _generate_verbose_names(name)
        cls._meta.verbose_name = singular
        cls._meta.verbose_name_plural = plural

        return cls


class BaseModel(models.Model, metaclass=BaseModelMeta):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


__all__ = ["BaseModel"]
