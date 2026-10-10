from django.template import loader, TemplateDoesNotExist

from authn.models.session import Code
from bot.handlers.common import UserRejectReason
from notifications.email.sender import send_transactional_email
from notifications.helpers import generate_notification_token
from users.models.user import User


def send_registration_email(user: User):
    registration_template = loader.get_template("emails/registration.html")
    send_transactional_email(
        recipient=user.email,
        subject=f"Оплата получена, добро пожаловать!",
        html=registration_template.render({"user": user}),
        tags=["registration"]
    )


def send_renewal_email(user: User):
    renewal_template = loader.get_template("emails/renewal.html")
    send_transactional_email(
        recipient=user.email,
        subject=f"Членство в Клубе продлено",
        html=renewal_template.render({"user": user}),
        tags=["renewal"]
    )


def send_welcome_drink(user: User):
    welcome_drink_template = loader.get_template("emails/welcome.html")
    send_transactional_email(
        recipient=user.email,
        subject=f"Добро пожаловать в Клуб!",
        html=welcome_drink_template.render({
            "user": user,
            "secret_code": generate_notification_token(user),
        }),
        tags=["welcome"]
    )


def send_user_rejected_email(user: User, reason: UserRejectReason):
    try:
        rejected_template = loader.get_template(f"emails/rejected/{reason.value}.html")
    except TemplateDoesNotExist:
        rejected_template = loader.get_template(f"emails/rejected/intro.html")

    send_transactional_email(
        recipient=user.email,
        subject=f"Профиль пока не прошёл модерацию",
        html=rejected_template.render({"user": user}),
        tags=["rejected"]
    )


def send_auth_email(user: User, code: Code):
    auth_template = loader.get_template("emails/auth.html")
    send_transactional_email(
        recipient=user.email,
        subject=f"{code.code} — ваш код для входа",
        html=auth_template.render({"user": user, "code": code}),
        tags=["auth"]
    )


def send_unmoderated_email(user: User):
    rejected_template = loader.get_template("emails/unmoderated.html")
    send_transactional_email(
        recipient=user.email,
        subject=f"Нужно дополнить профиль",
        html=rejected_template.render({"user": user}),
        tags=["unmoderated"]
    )


def send_banned_email(user: User, days: int, reason: str):
    if not user.is_banned or not days:
        return  # not banned oO

    banned_template = loader.get_template("emails/banned.html")
    send_transactional_email(
        recipient=user.email,
        subject=f"Ваш аккаунт заблокирован",
        html=banned_template.render({
            "user": user,
            "days": days,
            "reason": reason,
        }),
        tags=["banned"]
    )


def send_ping_email(user: User, message: str):
    ping_template = loader.get_template("emails/ping.html")
    send_transactional_email(
        recipient=user.email,
        subject=f"👋 Вам письмо",
        html=ping_template.render({"message": message}),
        tags=["ping"]
    )


def send_data_archive_ready_email(user: User, url: str):
    auth_template = loader.get_template("emails/data_archive_ready.html")
    send_transactional_email(
        recipient=user.email,
        subject=f"💽 Ваш архив с данными готов",
        html=auth_template.render({"user": user, "url": url}),
        tags=["gdpr"]
    )


def send_delete_account_request_email(user: User, code: Code):
    auth_template = loader.get_template("emails/delete_account_request.html")
    send_transactional_email(
        recipient=user.email,
        subject=f"Код для удаления аккаунта",
        html=auth_template.render({"user": user, "code": code}),
        tags=["killme"]
    )


def send_delete_account_confirm_email(user: User):
    auth_template = loader.get_template("emails/delete_account_confirm.html")
    send_transactional_email(
        recipient=user.email,
        subject=f"Ваш аккаунт в Клубе будет удалён",
        html=auth_template.render({"user": user}),
        tags=["killme"]
    )
