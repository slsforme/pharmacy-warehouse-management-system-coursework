import uuid

from django.db import models
from deep_translator import GoogleTranslator
from mawo_pymorphy3 import create_analyzer

analyzer = create_analyzer()
translator = GoogleTranslator(source='en', target='ru')

def _translate_text(text: str):
    return translator.translate(text)

def _get_plural_form(name: str):
    singular_form_word = _get_singular_form_name(name)
    plural_form_word = analyzer.parse(singular_form_word)[0]

def _get_singular_form_name(name: str):
    return _translate_text(name)

class BaseModel(models.Model):
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    class Meta:
        abstract = True
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        
        if cls._meta.abstract:
            return
        
        singular = _translate_text(cls.__name__)
        plural = _get_plural_form(singular)
        
        cls._meta.verbose_name = singular
        cls._meta.verbose_name_plural = plural

__all__ = ["BaseModel"]
