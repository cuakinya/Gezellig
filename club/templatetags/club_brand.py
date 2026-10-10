"""
Брендинг клуба в шаблонах. Подключён как builtin (см. TEMPLATES в settings.py),
поэтому работает везде — на страницах, в письмах и в телеграм-сообщениях — без {% load %}.

    {% club_name %}              -> Хезеллих
    {% club_url %}               -> https://домен-клуба
    {% club_email %}             -> общий контактный адрес
    {% club_email "moderator" %} -> адрес модераторов
    {% club_email "payments" %}  -> адрес по вопросам оплаты
"""
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def club_name():
    return settings.CLUB_NAME


@register.simple_tag
def club_url():
    return settings.APP_HOST


@register.simple_tag
def club_email(kind="contact"):
    return getattr(settings, f"CLUB_{kind.upper()}_EMAIL", settings.CLUB_CONTACT_EMAIL)
