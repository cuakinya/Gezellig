import logging
import uuid
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from yookassa import Configuration, Payment as YookassaPayment

from club.exceptions import BadRequest
from payments.exceptions import PaymentException
from payments.helpers import parse_yookassa_webhook_event
from payments.models import Payment
from payments.products import find_yookassa_product, YOOKASSA_DEFAULT_PRODUCT_CODE, YOOKASSA_INVITE_PRODUCT
from users.models.user import User

log = logging.getLogger()

Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_API_KEY


def pay(request):
    """Разовая покупка периода членства (или инвайта) через ЮKassa: создаём платёж и уводим на страницу оплаты"""
    if not settings.YOOKASSA_SHOP_ID or not settings.YOOKASSA_API_KEY:
        return render(request, "error.html", {
            "title": "Оплата ещё не настроена",
            "message": "Укажите YOOKASSA_SHOP_ID и YOOKASSA_API_KEY в настройках (для начала — ключи тестового магазина)."
        })

    product_code = request.GET.get("product_code") or YOOKASSA_DEFAULT_PRODUCT_CODE
    product = find_yookassa_product(product_code)
    if not product:
        return render(request, "error.html", {
            "title": "Не выбран пакет 😣",
            "message": "Выберите, на какой срок вы хотите вступить или продлить членство"
        })

    is_invite = product["code"] == YOOKASSA_INVITE_PRODUCT["code"]
    now = datetime.utcnow()

    if request.me:  # продление или покупка инвайта
        user = request.me
    else:  # новый участник
        if is_invite:
            return redirect("login")

        email = (request.GET.get("email") or "").lower().strip()
        if not email or "@" not in email:
            return render(request, "error.html", {
                "title": "Плохой e-mail адрес 😣",
                "message": "Нам ведь нужно будет как-то привязать аккаунт к платежу"
            })

        user, _ = User.objects.get_or_create(
            email=email,
            defaults=dict(
                membership_platform_type=User.MEMBERSHIP_PLATFORM_DIRECT,
                full_name=email[:email.find("@")],
                membership_started_at=now,
                membership_expires_at=now,
                created_at=now,
                updated_at=now,
                moderation_status=User.MODERATION_STATUS_INTRO,
            ),
        )

    session = YookassaPayment.create({
        "amount": {
            "value": product["amount"],
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": settings.APP_HOST + (reverse("invites") if is_invite else "/user/me/")
        },
        "capture": True,
        "description": f"{product['description']} для {user.email}",
        "metadata": {
            "email": user.email,
            "product": product["code"],
        },
        "receipt": {
            "customer": {
                "full_name": user.full_name,
                "email": user.email,
            },
            "items": [
                {
                    "description": product["description"],
                    "quantity": "1.00",
                    "amount": {
                        "value": product["amount"],
                        "currency": "RUB"
                    },
                    "payment_mode": "full_payment",
                    "payment_subject": "service",
                    "vat_code": 1,
                },
            ]
        }
    }, uuid.uuid4())

    Payment.create(
        reference=session.id,
        user=user,
        product=product,
        data=session.json(),
    )

    return redirect(session.confirmation.confirmation_url)


def yookassa_webhook(request):
    try:
        webhook = parse_yookassa_webhook_event(request)
    except BadRequest as ex:
        return HttpResponse(ex.message, status=ex.code)

    log.info(f"YOOKASSA WEBHOOK: {webhook.json()}")

    if webhook.event == "payment.succeeded":
        try:
            real_payment = YookassaPayment.find_one(webhook.object.id)
        except Exception as ex:
            log.error(
                f"Не удалось верифицировать платёж "
                f"{webhook.object.id} в ЮКассе: {ex}"
            )
            return HttpResponse("[verification failed]", status=400)

        # Проверяем статус из ответа API, а не из тела webhook
        if real_payment.status != "succeeded":
            log.warning(
                f"Статус платежа {webhook.object.id} "
                f"не совпадает: {real_payment.status}"
            )
            return HttpResponse("[invalid payment status]", status=400)

        # Берём email и product из верифицированного ответа ЮКассы
        email = real_payment.metadata.get("email")
        product_code = real_payment.metadata.get("product")

        if not email or not product_code:
            log.warning(
                f"Отсутствуют метаданные в платеже {webhook.object.id}"
            )
            return HttpResponse("[invalid metadata]", status=400)

        # Проверяем что продукт существует в нашем каталоге
        product = find_yookassa_product(product_code)
        if not product:
            log.warning(
                f"Неизвестный код продукта в платеже "
                f"{webhook.object.id}: {product_code}"
            )
            return HttpResponse("[unknown product]", status=400)

        user = User.objects.filter(email=email).first()

        try:
            payment = Payment.finish(
                reference=webhook.object.id,
                status=Payment.STATUS_SUCCESS,
                data=webhook.json(),
            )
        except PaymentException:
            return HttpResponse("[payment not found]", status=400)

        if not user:
            user = payment.user

        product["activator"](product, payment, user)
        return HttpResponse("[ok]", status=200)

    return HttpResponse("[unknown event]", status=200)
