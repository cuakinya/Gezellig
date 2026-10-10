import uuid
from datetime import datetime, timedelta
from types import SimpleNamespace
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse

from debug.helpers import HelperClient
from invites.models import Invite
from payments.models import Payment
from payments.products import YOOKASSA_PRODUCTS, YOOKASSA_INVITE_PRODUCT, YOOKASSA_DEFAULT_PRODUCT_CODE
from users.models.user import User

CONFIRMATION_URL = "https://yoomoney.ru/checkout/payments/v2/contract?orderId=test"


def fake_yookassa_session():
    return SimpleNamespace(
        id=f"yk-{uuid.uuid4()}",
        confirmation=SimpleNamespace(confirmation_url=CONFIRMATION_URL),
        json=lambda: "{}",
    )


@override_settings(YOOKASSA_SHOP_ID="test-shop", YOOKASSA_API_KEY="test-key")
@patch("payments.views.yookassa.YookassaPayment")
class TestYookassaPayView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.member = User.objects.create(
            email="member@example.com",
            membership_started_at=datetime.utcnow() - timedelta(days=5),
            membership_expires_at=datetime.utcnow() + timedelta(days=5),
            slug="member",
        )

    def test_new_user_redirected_to_yookassa(self, mocked_yookassa):
        session = fake_yookassa_session()
        mocked_yookassa.create.return_value = session
        email = f"new-{uuid.uuid4()}@example.com"

        response = self.client.get(reverse("pay"), data={"product_code": "club3m_ru", "email": email})

        self.assertRedirects(response, CONFIRMATION_URL, fetch_redirect_response=False)
        user = User.objects.get(email=email)
        self.assertEqual(user.moderation_status, User.MODERATION_STATUS_INTRO)
        payment = Payment.get(reference=session.id)
        self.assertEqual(payment.product_code, "club3m_ru")
        self.assertEqual(payment.user, user)

        sent = mocked_yookassa.create.call_args[0][0]
        self.assertEqual(sent["amount"], {"value": YOOKASSA_PRODUCTS["club3m_ru"]["amount"], "currency": "RUB"})
        self.assertEqual(sent["metadata"], {"email": email, "product": "club3m_ru"})

    def test_default_product_when_not_selected(self, mocked_yookassa):
        session = fake_yookassa_session()
        mocked_yookassa.create.return_value = session

        HelperClient(user=self.member).get(reverse("pay"))

        self.assertEqual(Payment.get(reference=session.id).product_code, YOOKASSA_DEFAULT_PRODUCT_CODE)

    def test_member_buys_invite(self, mocked_yookassa):
        session = fake_yookassa_session()
        mocked_yookassa.create.return_value = session

        response = HelperClient(user=self.member).get(
            reverse("pay"), data={"product_code": YOOKASSA_INVITE_PRODUCT["code"]}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Payment.get(reference=session.id).user, self.member)

    def test_anonymous_cannot_buy_invite(self, mocked_yookassa):
        response = self.client.get(
            reverse("pay"), data={"product_code": YOOKASSA_INVITE_PRODUCT["code"], "email": "x@example.com"}
        )

        self.assertRedirects(response, reverse("login"), fetch_redirect_response=False)
        mocked_yookassa.create.assert_not_called()

    def test_bad_email(self, mocked_yookassa):
        response = self.client.get(reverse("pay"), data={"product_code": "club1m_ru", "email": "nope"})

        self.assertContains(response, "Плохой e-mail", status_code=200)
        mocked_yookassa.create.assert_not_called()

    def test_unknown_product(self, mocked_yookassa):
        response = self.client.get(reverse("pay"), data={"product_code": "club50", "email": "a@example.com"})

        self.assertContains(response, "Не выбран пакет", status_code=200)
        mocked_yookassa.create.assert_not_called()

    def test_rubles_url_redirects_to_pay(self, mocked_yookassa):
        response = self.client.get("/rubles/?product_code=club1m_ru")

        self.assertRedirects(response, reverse("pay") + "?product_code=club1m_ru", fetch_redirect_response=False)


@override_settings(YOOKASSA_SHOP_ID="", YOOKASSA_API_KEY="")
class TestYookassaNotConfigured(TestCase):
    def test_shows_setup_hint(self):
        response = self.client.get(reverse("pay"), data={"email": "a@example.com"})

        self.assertContains(response, "Оплата ещё не настроена", status_code=200)


class TestYookassaActivation(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="buyer@example.com",
            membership_started_at=datetime.utcnow(),
            membership_expires_at=datetime.utcnow() - timedelta(days=10),
            slug="buyer",
        )

    def test_period_adds_days_from_now_when_expired(self):
        product = YOOKASSA_PRODUCTS["club1m_ru"]
        payment = Payment.create(reference="r1", user=self.user, product=product)

        product["activator"](product, payment, self.user)

        self.user.refresh_from_db()
        self.assertAlmostEqual(
            self.user.membership_expires_at, datetime.utcnow() + timedelta(days=31), delta=timedelta(seconds=10)
        )

    def test_invite_product_creates_invite(self):
        payment = Payment.create(reference="r2", user=self.user, product=YOOKASSA_INVITE_PRODUCT)

        YOOKASSA_INVITE_PRODUCT["activator"](YOOKASSA_INVITE_PRODUCT, payment, self.user)

        self.assertTrue(Invite.objects.filter(user=self.user, payment=payment).exists())


class TestPackagesBlock(TestCase):
    def test_join_page_shows_ruble_packages(self):
        response = self.client.get(reverse("join"))

        for product in YOOKASSA_PRODUCTS.values():
            self.assertContains(response, f'value="{product["code"]}"')
        self.assertContains(response, "₽")
        self.assertNotContains(response, "€")
