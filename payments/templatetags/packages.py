from decimal import Decimal

from django import template

from payments.products import YOOKASSA_PRODUCTS, YOOKASSA_DEFAULT_PRODUCT_CODE, YOOKASSA_INVITE_PRODUCT

register = template.Library()


def _price(amount):
    return f"{Decimal(amount):,.0f}".replace(",", " ")


@register.simple_tag
def club_packages():
    return [
        {
            "code": p["code"],
            "title": p["title"],
            "price": _price(p["amount"]),
            "is_default": p["code"] == YOOKASSA_DEFAULT_PRODUCT_CODE,
        }
        for p in YOOKASSA_PRODUCTS.values()
    ]


@register.simple_tag
def club_invite_package():
    return {
        "code": YOOKASSA_INVITE_PRODUCT["code"],
        "price": _price(YOOKASSA_INVITE_PRODUCT["amount"]),
    }
