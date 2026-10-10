# Миграция 0029 из движка vas3k.club создаёт служебных пользователей и тексты «О Клубе»,
# «Политика приватности» и т.д. с содержимым Вастрик.Клуба. Здесь они заменяются
# на черновики-заглушки нашего клуба, и добавляются гайды, на которые ссылаются настройки.
from datetime import datetime

from django.conf import settings
from django.db import migrations

DRAFT = "Черновик. Текст ещё не написан."

DOCS = [
    ("about", "О Клубе", DRAFT + "\n\nЗдесь будет рассказ о клубе: для кого он, что внутри, как вступить и какие правила."),
    ("values", "Наши ценности", DRAFT + "\n\nЗдесь будут ценности и правила поведения в клубе."),
    ("contact", "Связаться с нами", "По любым вопросам пишите на " + settings.CLUB_CONTACT_EMAIL + "."),
    ("privacy_policy", "Политика обработки персональных данных", DRAFT + "\n\nПолитика появится после консультации с юристом."),
    ("posting", "Как писать посты", DRAFT),
    ("chats", "Клубные чаты", DRAFT),
    ("people", "Карта участников", DRAFT),
]

OBSOLETE_DOCS = ["blocked_dolor"]  # гайд Вастрика по оплате из России, у нас оплата сразу в рублях


def forwards(apps, schema_editor):
    User = apps.get_model("users", "User")
    Post = apps.get_model("posts", "Post")
    now = datetime.utcnow()

    User.objects.filter(slug=settings.MODERATOR_USERNAME).update(
        email=settings.CLUB_MODERATOR_EMAIL,
        company=settings.CLUB_NAME,
        position="Модерирую",
        city=None,
        country=None,
    )
    User.objects.filter(slug=settings.DELETED_USERNAME).update(email="deleted@example.com", country=None)

    author = User.objects.filter(slug=settings.MODERATOR_USERNAME).first()
    if not author:
        return

    for slug, title, text in DOCS:
        Post.objects.update_or_create(
            slug=slug,
            defaults=dict(
                type="docs",
                title=title,
                text=text,
                html=None,
                author=author,
                updated_at=now,
                last_activity_at=now,
                published_at=now,
                visibility="link_only",  # открываются по ссылке, но не попадают в ленту
                moderation_status="approved",
                is_commentable=False,
                is_public=True,
            ),
        )

    Post.objects.filter(slug__in=OBSOLETE_DOCS, type="docs").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0037_alter_historicalpost_type_alter_post_type"),
        ("users", "0036_move_geo_to_map"),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
